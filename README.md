# Wave Path 2.0 × Quran-Core — Full Reference Implementation

This repository is a research/engineering reference implementation of a closed-loop architecture:

`Quran-Core (reference) → formal rule → model → observation → state → Wave Path → Lyapunov → risk → policy guard → enforcement → feedback`

## Important scientific boundary

The Quranic layer is represented as a **reference/interpretive layer**, not as a literal source of physical equations. The project records the text, interpretation context, extracted relation, and transformation rule separately from mathematical and empirical claims. Any physical model must be tested independently against observations.

The first methodological test uses Qur'an 41:53 as an observation/discernment framing. The wave equation and Lyapunov energy used in the demo are standard mathematical reference models; they are **not claimed to be derived from the verse**.

## What is executable here

- Python end-to-end deterministic demo: telemetry → state → Wave Path → Lyapunov → risk → policy → feedback.
- C++ Lyapunov reference engine.
- Rust state/risk/policy/controller implementation (source-complete; Rust toolchain required to compile).
- eBPF/XDP enforcement source with a safe default PASS policy and a bounded IPv4 blocklist map.
- Reproducible tests and JSON/CSV experiment outputs.

## Quick start

```bash
python3 scripts/run_demo.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Compile the C++ reference engine:

```bash
g++ -std=c++17 -O2 -Wall -Wextra -pedantic lyapunov/lyapunov_engine.cpp -o /tmp/wave-path-lyapunov
/tmp/wave-path-lyapunov
```

The Rust workspace can be compiled with Cargo on a machine with Rust installed:

```bash
cargo check --workspace
cargo test --workspace
```

The eBPF program requires a Linux eBPF development environment (kernel UAPI headers, libbpf headers, clang/LLVM and a userspace loader). This repository does not claim that kernel attachment was performed in this environment.

## Architecture

```text
                    +---------------------------+
                    |       QURAN-CORE          |
                    | text / context / relation |
                    | transformation provenance |
                    +-------------+-------------+
                                  |
                                  v
                    +---------------------------+
                    |      FORMAL MODEL          |
                    | hypothesis / model / test  |
                    +-------------+-------------+
                                  |
                                  v
REALITY ---> eBPF/XDP ---> TELEMETRY ---> STATE ---> WAVE PATH
   ^                                               |
   |                                               v
   |                                           LYAPUNOV
   |                                               |
   |                                               v
   |                                            RISK/AI
   |                                               |
   |                                               v
   +<--------- ACTION <------- POLICY GUARD <-------+
```

## No fabricated performance claims

The repository contains target/benchmark configuration, not proof of a specific latency such as 0.1 ms or 0.38 ms. Any production performance number must come from a reproducible benchmark on a specified machine, kernel, compiler and workload.
