#include <cmath>
#include <iomanip>
#include <iostream>

struct State { double u; double v; };

double V(const State& x, double omega) {
    return 0.5 * (x.v*x.v + omega*omega*x.u*x.u);
}

double dVdt_estimate(const State& a, const State& b, double omega, double dt) {
    if (dt <= 0.0) return 0.0;
    return (V(b, omega) - V(a, omega)) / dt;
}

int main() {
    const double omega = 2.0 * M_PI;
    const double dt = 0.001;
    const State a{1.0, 0.0};
    const State b{0.999, -0.039};
    std::cout << std::setprecision(12)
              << "V(a)=" << V(a, omega) << "\n"
              << "V(b)=" << V(b, omega) << "\n"
              << "dVdt=" << dVdt_estimate(a,b,omega,dt) << "\n";
    return 0;
}
