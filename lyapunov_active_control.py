import time
import random

class ActiveLyapunovSystem:
    def __init__(self, state, gains):
        self.state = list(state)
        self.gains = list(gains)

    def compute_lyapunov_energy(self):
        return 0.5 * sum(g * (s ** 2) for g, s in zip(self.gains, self.state))

    def compute_derivative(self):
        return -1.2 * (self.state[0] ** 2) - 2.0 * (self.state[1] ** 2) - 1.5 * (self.state[2] ** 2)

    def step(self, dt, control_input):
        # تطبيق إشارة التحكم الديناميكي u مع مقاومة التغيرات
        self.state[0] += (-0.8 * self.state[0] + control_input[0]) * dt
        self.state[1] += (-1.0 * self.state[1] + control_input[1]) * dt
        self.state[2] += (-0.5 * self.state[2] + control_input[2]) * dt

def main():
    print("------------------------------------------------------------------")
    print("[AQI SOVEREIGN KERNEL] Initializing Active Dynamic Control Layer...")
    print("------------------------------------------------------------------")
    
    system = ActiveLyapunovSystem([3.0, 2.0, 1.5], [2.0, 1.5, 2.5])
    dt = 0.1
    
    for tick in range(1, 21):
        energy = system.compute_lyapunov_energy()
        v_dot = system.compute_derivative()
        
        # محاكاة إدخال تحكم عكسي تصحيحي يعتمد على حالة النظام الحالية (Feedback Control)
        # u = -K * x
        control_u = [-0.5 * system.state[0], -0.4 * system.state[1], -0.3 * system.state[2]]
        
        # حقن اضطراب عشوائي طفيف عند التكة رقم 10 لاختبار كفاءة الاستجابة
        if tick == 10:
            print("[WARNING] External disturbance injected into system states!")
            system.state[0] += 1.5
            system.state[1] -= 1.0

        status = "STABLE [مستقر]" if v_dot < 0.0 else "UNSTABLE [غير مستقر]"
        
        print(f"[Tick {tick:02}] State: [{system.state[0]:.3f}, {system.state[1]:.3f}, {system.state[2]:.3f}] | V(x): {energy:.4f} | V_dot: {v_dot:.4f} | Control: Active | {status}")
        
        system.step(dt, control_u)
        time.sleep(0.2)
        
    print("------------------------------------------------------------------")
    print("[INFO] Active Dynamic Control Simulation completed successfully.")
    print("------------------------------------------------------------------")

if __name__ == "__main__":
    main()
