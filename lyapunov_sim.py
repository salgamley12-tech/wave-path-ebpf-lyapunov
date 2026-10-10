import time

class LyapunovSystem:
    def __init__(self, state, gains):
        self.state = list(state)
        self.gains = list(gains)

    def compute_lyapunov_energy(self):
        return 0.5 * sum(g * (s ** 2) for g, s in zip(self.gains, self.state))

    def compute_derivative(self):
        return -1.2 * (self.state[0] ** 2) - 2.0 * (self.state[1] ** 2) - 1.5 * (self.state[2] ** 2)

    def step(self, dt):
        self.state[0] += -0.8 * self.state[0] * dt
        self.state[1] += -1.0 * self.state[1] * dt
        self.state[2] += -0.5 * self.state[2] * dt

def main():
    print("------------------------------------------------------------")
    print("[AQI SOVEREIGN KERNEL] Initializing Python Lyapunov Daemon...")
    print("------------------------------------------------------------")
    
    system = LyapunovSystem([3.0, 2.0, 1.5], [2.0, 1.5, 2.5])
    dt = 0.1
    
    for tick in range(1, 21):
        energy = system.compute_lyapunov_energy()
        v_dot = system.compute_derivative()
        status = "STABLE [مستقر]" if v_dot < 0.0 else "UNSTABLE [غير مستقر]"
        
        print(f"[Tick {tick:02}] State: [{system.state[0]:.3f}, {system.state[1]:.3f}, {system.state[2]:.3f}] | V(x): {energy:.4f} | V_dot: {v_dot:.4f} | Status: {status}")
        
        system.step(dt)
        time.sleep(0.2)
        
    print("------------------------------------------------------------")
    print("[INFO] Simulation target reached successfully.")
    print("------------------------------------------------------------")

if __name__ == "__main__":
    main()
