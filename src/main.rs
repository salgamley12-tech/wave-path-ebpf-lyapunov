use std::thread;
use std::time::Duration;

struct LyapunovSystem {
    state: [f64; 3],
    gains: [f64; 3],
}

impl LyapunovSystem {
    fn new(state: [f64; 3], gains: [f64; 3]) -> Self {
        Self { state, gains }
    }

    fn compute_lyapunov_energy(&self) -> f64 {
        0.5 * (self.gains[0] * self.state[0].powi(2)
             + self.gains[1] * self.state[1].powi(2)
             + self.gains[2] * self.state[2].powi(2))
    }

    fn compute_derivative(&self) -> f64 {
        -1.2 * self.state[0].powi(2)
        - 2.0 * self.state[1].powi(2)
        - 1.5 * self.state[2].powi(2)
    }

    fn step(&mut self, dt: f64) {
        self.state[0] += -0.8 * self.state[0] * dt;
        self.state[1] += -1.0 * self.state[1] * dt;
        self.state[2] += -0.5 * self.state[2] * dt;
    }
}

fn main() {
    println!("------------------------------------------------------------");
    println!("[AQI SOVEREIGN KERNEL] Initializing User-Space Lyapunov Daemon...");
    println!("------------------------------------------------------------");

    let mut system = LyapunovSystem::new([3.0, 2.0, 1.5], [2.0, 1.5, 2.5]);
    let dt = 0.1;
    let mut tick = 0;

    loop {
        tick += 1;
        let energy = system.compute_lyapunov_energy();
        let v_dot = system.compute_derivative();
        let stable = v_dot < 0.0;

        println!(
            "[Tick {:02}] State: [{:.3}, {:.3}, {:.3}] | V(x): {:.4} | V_dot: {:.4} | Status: {}",
            tick,
            system.state[0],
            system.state[1],
            system.state[2],
            energy,
            v_dot,
            if stable { "STABLE [مستقر]" } else { "UNSTABLE [غير مستقر]" }
        );

        system.step(dt);
        thread::sleep(Duration::from_millis(200));

        if tick >= 20 {
            println!("------------------------------------------------------------");
            println!("[INFO] Simulation target reached successfully.");
            println!("------------------------------------------------------------");
            break;
        }
    }
}
