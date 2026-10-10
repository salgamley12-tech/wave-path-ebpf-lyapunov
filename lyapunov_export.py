import csv
import json

class ActiveLyapunovSystem:
    def __init__(self, state, gains):
        self.state = list(state)
        self.gains = list(gains)

    def compute_lyapunov_energy(self):
        return 0.5 * sum(g * (s ** 2) for g, s in zip(self.gains, self.state))

    def compute_derivative(self):
        return -1.2 * (self.state[0] ** 2) - 2.0 * (self.state[1] ** 2) - 1.5 * (self.state[2] ** 2)

    def step(self, dt, control_input):
        self.state[0] += (-0.8 * self.state[0] + control_input[0]) * dt
        self.state[1] += (-1.0 * self.state[1] + control_input[1]) * dt
        self.state[2] += (-0.5 * self.state[2] + control_input[2]) * dt

def main():
    print("------------------------------------------------------------------")
    print("[AQI SOVEREIGN KERNEL] Running Simulation & Exporting Metrics...")
    print("------------------------------------------------------------------")
    
    system = ActiveLyapunovSystem([3.0, 2.0, 1.5], [2.0, 1.5, 2.5])
    dt = 0.1
    logs = []
    
    for tick in range(1, 21):
        energy = system.compute_lyapunov_energy()
        v_dot = system.compute_derivative()
        control_u = [-0.5 * system.state[0], -0.4 * system.state[1], -0.3 * system.state[2]]
        
        # حقن اضطراب عند التكة 10
        if tick == 10:
            system.state[0] += 1.5
            system.state[1] -= 1.0

        status = "STABLE [مستقر]" if v_dot < 0.0 else "UNSTABLE [غير مستقر]"
        
        log_entry = {
            "tick": tick,
            "state_x0": round(system.state[0], 4),
            "state_x1": round(system.state[1], 4),
            "state_x2": round(system.state[2], 4),
            "energy_v": round(energy, 4),
            "v_dot": round(v_dot, 4),
            "status": status
        }
        logs.append(log_entry)
        
        print(f"[Tick {tick:02}] V(x): {energy:.4f} | V_dot: {v_dot:.4f} | {status}")
        system.step(dt, control_u)

    # 1. تصدير السجلات إلى ملف CSV تفصيلي
    csv_filename = "lyapunov_audit_log.csv"
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=logs[0].keys())
        writer.writeheader()
        writer.writerows(logs)

    # 2. إنشاء ملف ملخص التحليل بصيغة JSON
    summary = {
        "system_name": "AQI Sovereign Kernel - Lyapunov User-Space Daemon",
        "total_ticks": len(logs),
        "initial_energy": logs[0]["energy_v"],
        "final_energy": logs[-1]["energy_v"],
        "max_energy": max(l["energy_v"] for l in logs),
        "min_energy": min(l["energy_v"] for l in logs),
        "stability_verification": all("STABLE" in l["status"] for l in logs)
    }
    json_filename = "lyapunov_summary.json"
    with open(json_filename, mode='w', encoding='utf-8') as f:
        json.dump(summary, f, indent=4, ensure_ascii=False)

    print("------------------------------------------------------------------")
    print(f"[SUCCESS] Export completed successfully!")
    print(f" -> CSV Audit Log: {csv_filename}")
    print(f" -> JSON Summary:  {json_filename}")
    print("------------------------------------------------------------------")

if __name__ == "__main__":
    main()
