#!/data/data/com.termux/files/usr/bin/env python3
import time
import datetime

class AlertingLyapunovDaemon:
    def __init__(self, state, gains, alert_log_file="lyapunov_system_alerts.log"):
        self.state = list(state)
        self.gains = list(gains)
        self.alert_log_file = alert_log_file
        self.running = True

    def compute_energy(self):
        return 0.5 * sum(g * (s ** 2) for g, s in zip(self.gains, self.state))

    def compute_derivative(self):
        return -1.2 * (self.state[0] ** 2) - 2.0 * (self.state[1] ** 2) - 1.5 * (self.state[2] ** 2)

    def log_alert(self, level, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        with open(self.alert_log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)
        print(f" -> [ALERT WRITTEN TO FILE] {level}: {message}")

    def update_states(self, dt, external_disturbance=0.0):
        # تطبيق التحكم العكسي مع احتمالية حدوث اضطراب خارجي
        u = [-0.5 * self.state[0], -0.4 * self.state[1], -0.3 * self.state[2]]
        self.state[0] += (-0.8 * self.state[0] + u[0] + external_disturbance) * dt
        self.state[1] += (-1.0 * self.state[1] + u[1]) * dt
        self.state[2] += (-0.5 * self.state[2] + u[2]) * dt

    def run_daemon(self, interval=1.0, max_ticks=15):
        print("------------------------------------------------------------------")
        print("[AQI SOVEREIGN KERNEL] Alerting Lyapunov Daemon Initialized...")
        print(f"[INFO] Audit trail target: {self.alert_log_file}")
        print("------------------------------------------------------------------")
        
        self.log_alert("INFO", "Daemon service started successfully in user-space.")
        tick = 0
        
        try:
            while self.running and tick < max_ticks:
                tick += 1
                
                # حقن اضطراب تجريبي عند التكة رقم 6 لاختبار نظام الإنذار
                disturbance = 2.0 if tick == 6 else 0.0
                if disturbance != 0.0:
                    print(f"\n[WARNING] Simulated external system shock injected at Tick {tick}!")
                    self.log_alert("WARNING", f"External system shock injected. State destabilization pressure applied.")

                energy = self.compute_energy()
                v_dot = self.compute_derivative()
                
                # فحص عتبة الاستقرار
                if v_dot >= 0.0:
                    status = "UNSTABLE [تحذير: غير مستقر]"
                    self.log_alert("CRITICAL", f"Stability loss detected! V_dot: {v_dot:.4f}, Energy V(x): {energy:.4f}")
                else:
                    status = "STABLE [مستقر]"

                print(f"[TICK {tick:02}] Energy V(x): {energy:.4f} | V_dot: {v_dot:.4f} | Status: {status}")
                
                self.update_states(0.1, external_disturbance=disturbance)
                time.sleep(interval)
                
            self.log_alert("INFO", "Daemon heartbeat cycle completed successfully.")
            print("------------------------------------------------------------------")
            print("[INFO] Daemon execution finished. Audit log updated.")
            print("------------------------------------------------------------------")
            
        except KeyboardInterrupt:
            self.log_alert("ERROR", "Daemon service terminated manually by user interrupt.")
            print("\n[INFO] Daemon stopped by user signal.")

if __name__ == "__main__":
    daemon = AlertingLyapunovDaemon([3.0, 2.0, 1.5], [2.0, 1.5, 2.5])
    daemon.run_daemon()
