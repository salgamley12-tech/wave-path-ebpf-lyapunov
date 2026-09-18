"""EXP-012: Wave -> Observation -> Lyapunov -> Wave Path integration.

Uses the actual project components.
No real network traffic is generated.
"""

import csv
import json
import math

from model.wave.damped_wave import Config, run
from model.observation.observation import observe, rmse
from lyapunov.lyapunov import oscillator_energy, finite_difference
from wave_path.path import WavePath, PathPoint


OUTPUT_CSV = "experiments/integrated/EXP_012_wave_observation.csv"
OUTPUT_JSON = "experiments/integrated/EXP_012_wave_observation.json"


def main():
    cfg = Config(
        seconds=2.0,
        dt=0.001,
        omega=2.0 * math.pi,
        damping=0.35,
        u0=1.0,
        v0=0.0,
    )

    # 1. Generate the actual deterministic wave model.
    wave_rows = run(cfg)

    # 2. Build observations from the actual wave signal.
    signal = [(row[0], row[1]) for row in wave_rows]
    observations = observe(signal, sigma=0.0, seed=7)

    # 3. Verify observation fidelity.
    predicted = [row[1] for row in wave_rows]
    observed = [item.value for item in observations]
    observation_rmse = rmse(predicted, observed)

    # 4. Build the actual Wave Path from the model trajectory.
    path = WavePath()

    rows = []
    previous_v_value = None
    previous_t = None

    for row, obs in zip(wave_rows, observations):
        t, u, v, model_V, model_dVdt = row

        # Recalculate V through the actual Lyapunov module.
        V = oscillator_energy(obs.value, v, cfg.omega)

        if previous_v_value is None:
            dVdt = 0.0
        else:
            dt = t - previous_t
            dVdt = finite_difference(previous_v_value, V, dt)

        path.append(
            PathPoint(
                t=t,
                state=(obs.value, v),
                V=V,
                dVdt=dVdt,
                risk="low",
                action="pass",
            )
        )

        rows.append(
            {
                "t": t,
                "u_model": u,
                "u_observed": obs.value,
                "v": v,
                "V_model": model_V,
                "V": V,
                "dVdt_model": model_dVdt,
                "dVdt": dVdt,
                "noise": obs.noise,
            }
        )

        previous_v_value = V
        previous_t = t

    # 5. Integrity measurements.
    initial_V = rows[0]["V"]
    final_V = rows[-1]["V"]
    minimum_V = min(item["V"] for item in rows)
    maximum_V = max(item["V"] for item in rows)

    max_abs_noise = max(abs(item["noise"]) for item in rows)

    V_errors = [
        abs(item["V"] - item["V_model"])
        for item in rows
    ]

    result = {
        "experiment": "EXP-012",
        "description": (
            "Integration validation of the actual wave model, observation "
            "layer, Lyapunov calculation, and Wave Path trajectory."
        ),
        "configuration": {
            "seconds": cfg.seconds,
            "dt": cfg.dt,
            "omega": cfg.omega,
            "damping": cfg.damping,
            "u0": cfg.u0,
            "v0": cfg.v0,
        },
        "samples": len(rows),
        "observation": {
            "sigma": 0.0,
            "seed": 7,
            "rmse": observation_rmse,
            "max_abs_noise": max_abs_noise,
        },
        "lyapunov": {
            "initial_V": initial_V,
            "final_V": final_V,
            "minimum_V": minimum_V,
            "maximum_V": maximum_V,
            "maximum_V_model_difference": max(V_errors),
        },
        "wave_path": {
            "points": len(path.points),
            "displacement": path.displacement(),
            "monotonic_time": all(
                rows[i]["t"] >= rows[i - 1]["t"]
                for i in range(1, len(rows))
            ),
        },
        "validation": {
            "sample_count_correct": len(rows) == 2001,
            "observation_rmse_zero": observation_rmse == 0.0,
            "noise_zero": max_abs_noise == 0.0,
            "wave_path_points_correct": len(path.points) == len(rows),
            "finite_values": all(
                math.isfinite(value)
                for item in rows
                for value in (
                    item["t"],
                    item["u_model"],
                    item["u_observed"],
                    item["v"],
                    item["V"],
                    item["dVdt"],
                )
            ),
        },
    }

    result["validation"]["validation_passed"] = all(
        result["validation"].values()
    )

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
