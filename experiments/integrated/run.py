"""Integrated Wave Path runtime.

Synthetic defensive telemetry -> state -> Lyapunov -> risk -> policy -> path.
No real network traffic is generated.
"""

import json

from experiments.cybersecurity.synthetic_stream import generate
from telemetry.aggregator import WindowAggregator
from model.state.state import State
from lyapunov.lyapunov import oscillator_energy, finite_difference
from controller.controller import Controller


def anomaly_score(event, features, baseline_bytes=100.0):
    """Deterministic synthetic anomaly score for the reference experiment."""
    score = 0.0

    if not event.authorized:
        score += 0.75

    if event.bytes > baseline_bytes:
        score += min(0.25, (event.bytes - baseline_bytes) / 2000.0)

    return min(score, 1.0)


def run():
    aggregator = WindowAggregator(window=1.0)
    controller = Controller()

    previous_v = None
    previous_t = None

    results = []

    for event in generate(200):
        aggregator.add(event)
        features = aggregator.features()

        state = State(
            bytes_rate=features["bytes_rate"],
            syscall_rate=features["syscall_rate"],
            connection_rate=features["connection_rate"],
            anomaly_score=anomaly_score(event, features),
        )

        # Normalize the telemetry channels for the energy model.
        u = state.bytes_rate / 100.0
        v = state.connection_rate / 10.0
        omega = 1.0

        V = oscillator_energy(u, v, omega)

        if previous_v is None:
            dVdt = 0.0
        else:
            dt = event.timestamp - previous_t
            dVdt = finite_difference(previous_v, V, dt)

        risk, action = controller.process(
            t=event.timestamp,
            state=(
                state.bytes_rate,
                state.syscall_rate,
                state.connection_rate,
                state.anomaly_score,
            ),
            V=V,
            dVdt=dVdt,
            anomaly_score=state.anomaly_score,
            authorized=event.authorized,
        )

        results.append({
            "t": event.timestamp,
            "bytes_rate": state.bytes_rate,
            "connection_rate": state.connection_rate,
            "anomaly_score": state.anomaly_score,
            "V": V,
            "dVdt": dVdt,
            "risk": risk.value,
            "action": action.value,
            "authorized": event.authorized,
        })

        previous_v = V
        previous_t = event.timestamp

    actions = {}
    risks = {}

    for item in results:
        actions[item["action"]] = actions.get(item["action"], 0) + 1
        risks[item["risk"]] = risks.get(item["risk"], 0) + 1

    output = {
        "samples": len(results),
        "risks": risks,
        "actions": actions,
        "initial_V": results[0]["V"],
        "final_V": results[-1]["V"],
        "path_points": len(controller.path.points),
        "path_displacement": controller.path.displacement(),
        "unauthorized_events": sum(
            1 for x in results if not x["authorized"]
        ),
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    run()
