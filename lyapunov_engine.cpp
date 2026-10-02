#include <iostream>
#include <cmath>

struct SystemState { double bytes_exfiltrated_rate; double unauthorized_syscalls; };

class LyapunovGuardrail {
private:
    double alpha, P11, P22;
public:
    LyapunovGuardrail(double conv_rate = 2.5) : alpha(conv_rate), P11(1.0), P22(1.5) {}
    double compute_V(const SystemState& x) const {
        return 0.5 * (P11 * std::pow(x.bytes_exfiltrated_rate, 2) + P22 * std::pow(x.unauthorized_syscalls, 2));
    }
    bool evaluate_and_enforce(const SystemState& x_curr, const SystemState& x_prev, double dt) {
        double V_curr = compute_V(x_curr), V_prev = compute_V(x_prev);
        double V_dot = (V_curr - V_prev) / dt;
        if (V_dot > -alpha * V_curr && V_curr > 0.01) {
            std::cout << "[CRITICAL ALERT] Lyapunov Instability Detected!" << std::endl;
            return false;
        }
        return true;
    }
};

int main() {
    LyapunovGuardrail guard(3.0);
    SystemState prev{0.0, 0.0}, curr{120.5, 4.0};
    guard.evaluate_and_enforce(curr, prev, 0.00038);
    return 0;
}
