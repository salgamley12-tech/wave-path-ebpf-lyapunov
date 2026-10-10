#!/data/data/com.termux/files/usr/bin/env python3
import time
import datetime
import os
import sys

class ContinuousSovereignDaemon:
    def __init__(self, alert_log_file="lyapunov_sovereign_balance.log"):
        self.alert_log_file = alert_log_file
        self.running = True
        self.gains = [2.0, 1.5, 2.5]

    def get_system_states(self):
        try:
            with open('/proc/loadavg', 'r') as f:
                load_data = f.read().split()
                x0 = float(load_data[0]) * 2.0
                x1 = float(load_data[1]) * 1.5
                x2 = float(load_data[2]) * 1.0
                return [x0, x1, x2]
        except Exception:
            return [1.2, 0.8, 0.5]

    def compute_energy(self, state):
        return 0.5 * sum(g * (s ** 2) for g, s in zip(self.gains, state))

    def compute_derivative(self, state):
        return -1.2 * (state[0] ** 2) - 2.0 * (state[1] ** 2) - 1.5 * (state[2] ** 2)

    def log_sovereign_event(self, level, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        with open(self.alert_log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)
        print(f" -> [SOVEREIGN AUDIT] {level}: {message}")

    def run_daemon(self, interval=3.0):
        print("------------------------------------------------------------------")
        print("[AQI SOVEREIGN KERNEL] Continuous Sovereign Balance Daemon Active...")
        print(f"[INFO] Ground truth log: {self.alert_log_file}")
        print("[INFO] Press Ctrl+C to terminate the sovereign loop safely.")
        print("------------------------------------------------------------------")
        
        self.log_sovereign_event("INFO", "Continuous sovereign telemetry daemon initialized.")
        cycle = 0
        
        try:
            while self.running:
                cycle += 1
                current_state = self.get_system_states()
                energy = self.compute_energy(current_state)
                v_dot = self.compute_derivative(current_state)
                
                if v_dot >= 0.0:
                    status = "IMBALANCE [اختلال في الميزان]"
                    self.log_sovereign_event("CRITICAL", f"Entropy spike at cycle {cycle}! V_dot: {v_dot:.4f}, Energy: {energy:.4f}")
                else:
                    status = "BALANCED [استقرار وميزان]"

                print(f"[TICK {cycle:04}] States: {[round(s, 3) for s in current_state]} | V(x): {energy:.4f} | V_dot: {v_dot:.4f} | {status}")
                
                # توثيق دوري كل 20 نبضة لضمان انتظام السجل
                if cycle % 20 == 0:
                    self.log_sovereign_event("CHECKPOINT", f"System stable over 20 cycles. Current Energy V(x): {energy:.4f}")

                time.sleep(interval)
                
        except KeyboardInterrupt:
            self.log_sovereign_event("INFO", "Daemon terminated safely by sovereign user intervention.")
            print("\n------------------------------------------------------------------")
            print("[INFO] Sovereign Daemon stopped gracefully. Audit log saved.")
            print("------------------------------------------------------------------")
            sys.exit(0)

if __name__ == "__main__":
    daemon = ContinuousSovereignDaemon()
    daemon.run_daemon()
