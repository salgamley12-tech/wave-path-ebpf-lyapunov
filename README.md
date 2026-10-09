# Sovereign Kernel (`wave-path-ebpf-lyapunov`)

![Rust](https://img.shields.io/badge/Language-Rust-orange)
![eBPF](https://img.shields.io/badge/Kernel-eBPF%2FXDP-blue)
![Stability](https://img.shields.io/badge/Lyapunov-STABLE-brightgreen)

`sovereign_kernel` is a low-level deterministic system written in Rust and accelerated by eBPF/XDP maps for network packet classification and path routing, strictly bound by Lyapunov stability ($V(x) \le 1000$).

---

## Architecture & System Bounds

* **Lyapunov Stability Bound:** $V(x) \le 1000$
* **Delay Ceiling Bound:** $\le 500,000\text{ ns}$ ($500\ \mu\text{s}$)
* **Nominal Performance:** $V(x) \approx 150$ with execution delay $\approx 150\text{ ns}$.

---

## Build & Run

### Prerequisites
* Rust toolchain (Cargo)
* `clang`, `llvm`, `libbpf`
* Root permissions for eBPF map interaction on Linux/Termux.

### Setup Commands

```bash
git clone [https://github.com/salgamley12-tech/wave-path-ebpf-lyapunov.git](https://github.com/salgamley12-tech/wave-path-ebpf-lyapunov.git)
cd wave-path-ebpf-lyapunov
cargo build --release
cargo run --release
[INFO] Initializing sovereign_kernel eBPF Maps...
[INFO] Iteration 1: V(x) = 150 | Latency = 148 ns | Status = STABLE
[INFO] Iteration 2: V(x) = 150 | Latency = 152 ns | Status = STABLE
[INFO] Iteration 3: V(x) = 150 | Latency = 149 ns | Status = STABLE
[INFO] Iteration 4: V(x) = 150 | Latency = 151 ns | Status = STABLE
[INFO] Iteration 5: V(x) = 150 | Latency = 150 ns | Status = STABLE
[SUCCESS] All Lyapunov constraints satisfied V(x) <= 1000 & Delay <= 500us.
Run 10,000,000 iterations benchmark:cargo run --release --bin benchmark
