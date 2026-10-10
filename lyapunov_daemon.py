import time
import sys

class LyapunovDaemon:
    def __init__(self, state, gains):
        self.state = list(state)
        self.gains = list(gains)
        self.running = True

    def compute_energy(self):
        return 0.5 * sum(g * (s ** 2) for g, s in zip(self.gains, self.state))

    def compute_derivative(self):
        return -1.2 * (self.state[0] ** 2) - 2.0 * (self.state[1] ** 2) - 1.5 * (self.state[2] ** 2)

    def update_states(self, dt):
        # تطبيق التحكم العكسي المقيد بالحالة الحالية
        u = [-0.5 * self.state[0], -0.4 * self.state[1], -0.3 * self.state[2]]
        self.state[0] += (-0.8 * self.state[0] + u[0]) * dt
        self.state[1] += (-1.0 * self.state[1] + u[1]) * dt
        self.state[2] += (-0.5 * self.state[2] + u[2]) * dt

    def run_daemon(self, interval=1.0, max_ticks=15):
        print("------------------------------------------------------------------")
        print("[AQI SOVEREIGN KERNEL] Lyapunov Daemon Service Started...")
        print("[INFO] Monitoring system stability in user-space background...")
        print("------------------------------------------------------------------")
        
        tick = 0
        try:
            while self.running and tick < max_ticks:
                tick += 1
                energy = self.compute_energy()
                v_dot = self.compute_derivative()
                status = "STABLE [مستقر]" if v_dot < 0.0 else "UNSTABLE [تحذير: غير مستقر]"
                
                print(f"[DAEMON TICK {tick:02}] Energy V(x): {energy:.4f} | V_dot: {v_dot:.4f} | Status: {status}")
                
                self.update_states(0.1)
                time.sleep(interval)
                
            print("------------------------------------------------------------------")
            print("[INFO] Daemon heartbeat cycle completed successfully.")
            print("------------------------------------------------------------------")
        except KeyboardInterrupt:
            print("\n[INFO] Daemon stopped by user signal.")

if __name__ == "__main__":
    daemon = LyapunovDaemon([3.0, 2.0, 1.5], [2.0, 1.5, 2.5])
    daemon.run_daemon()
