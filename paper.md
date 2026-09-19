# Wave Path 2.0: Reference-Constrained, Observation-Driven Control with Lyapunov-Like State Analysis and an eBPF/XDP Enforcement Boundary

**Author:** Sultan Ali Ali Algamley

**Affiliation:** Algamley Digital Engineering

**Repository:** `wave-path-ebpf-lyapunov`

**Branch:** `wave-path-2-integration`

**Manuscript status:** Reproducibility / research manuscript; not peer reviewed

---

## Abstract

Wave Path 2.0 is an experimental software architecture for connecting reference constraints, observation, state representation, Lyapunov-like analysis, risk classification, policy decisions, operational control, and an eBPF/XDP-oriented enforcement boundary. The project is designed around a strict methodological separation: a reference layer may define provenance and constraints, while mathematical models, algorithms, and empirical results remain independently testable engineering artifacts.

The present manuscript reports the repository's integrated synthetic experiments through EXP-013. EXP-001--EXP-011 establish the initial synthetic pipeline, trajectory analysis, response analysis, sensitivity testing, reproducibility check, consolidated report, and integrity audit. EXP-012 connects the damped-wave model, observation layer, Lyapunov calculation, and Wave Path under deterministic zero-noise conditions. EXP-013 extends that integration with controlled Gaussian observation noise (`sigma = 0.01`, seed `7`) while preserving the same computational path.

EXP-013 uses a 2.0 s simulation with `dt = 0.001`, `omega = 2π`, damping `0.35`, and initial state `(u0,v0)=(1,0)`. It generates 2,001 samples and 2,001 Wave Path points. The observed signal has RMSE `0.010126179713664026` relative to the model and maximum absolute injected noise `0.03444705105326818`. The observed-state energy-like quantity changes from `19.638320555259053` to `4.759952605748658`, with minimum `4.3793514684534065`, maximum `20.385783783522392`, and maximum model/observation energy difference `0.9140689456240736`. All programmed validation checks pass, and repeated execution with seed `7` is recorded as identical.

These results establish software-level synthetic integration and reproducibility under the tested configuration. They do **not** establish production-network performance, real eBPF/XDP latency, zero-exfiltration guarantees, AI detection accuracy, or a formal Lyapunov-stability theorem. The next experimental boundary is robustness analysis, interface validation, controlled eBPF/XDP integration, and reproducible benchmarking.

**Keywords:** Wave Path, eBPF, XDP, Lyapunov-like analysis, observation noise, policy control, risk classification, reproducibility, reference guard, synthetic experiments.

---

## 1. Introduction

Complex adaptive systems frequently combine several layers: a reference or specification layer, a mathematical model, observation, state estimation, decision logic, enforcement, and feedback. A central engineering problem is traceability: a system should make it possible to identify how an observation becomes a state, how the state is evaluated, how a policy decision is formed, and how that decision is translated into an operational action.

Wave Path 2.0 develops an experimental architecture around that traceability problem. The current repository expresses the integrated synthetic chain as:

```text
Synthetic Telemetry
        ↓
Window Aggregation / State Representation
        ↓
Lyapunov-like Energy V(x)
        ↓
dV/dt
        ↓
Risk Classification
        ↓
Policy Guard
        ↓
Action
        ↓
Wave Path
        ↓
Validation / Reproducibility
```

The newer integration experiments refine this chain by explicitly inserting an observation layer between the model and the state used by the Lyapunov calculation. EXP-012 provides the deterministic zero-noise baseline. EXP-013 introduces controlled observation noise and measures its effect on the observed trajectory.

The repository also contains a Quran-Core/reference concept. In this manuscript that layer is treated as a **conceptual and provenance layer**, not as a substitute for mathematical proof or empirical validation. The distinction is essential: a textual or religious reference can motivate a design principle within the project's conceptual framework, but a numerical claim remains a numerical claim and must be tested with independent engineering methods.

The eBPF/XDP portion is likewise bounded. eBPF is a Linux kernel mechanism for sandboxed runtime extension and instrumentation, while XDP provides a programmable packet-processing path in the kernel. The current repository identifies these technologies as an enforcement boundary, but the reported EXP-001--EXP-013 evidence is synthetic and does not constitute a live kernel benchmark. Linux documentation describes eBPF program verification, maps, program types, and kernel attachment mechanisms; the XDP literature provides the established background for programmable packet processing in driver context. [1--3]

---

## 2. Research Problem and Objectives

### 2.1 Problem

The research problem is how to construct an auditable control pipeline in which:

1. the reference layer is distinguishable from the mathematical model;
2. observation is distinguishable from the model's latent state;
3. state evaluation is explicit and reproducible;
4. policy intent is distinguishable from enforcement outcome;
5. every experimental claim can be connected to a persistent artifact;
6. future low-level enforcement can be integrated without retroactively treating simulation results as hardware measurements.

### 2.2 Objectives

The current implementation pursues the following objectives:

- construct an integrated synthetic pipeline;
- represent the system trajectory through Wave Path;
- calculate an energy-like state quantity and finite-difference derivative;
- test controlled observation noise;
- validate numerical and structural integrity;
- preserve reproducibility under deterministic inputs;
- expose policy/control integration points;
- maintain a clear experimental boundary before real eBPF/XDP benchmarking.

---

## 3. Conceptual Architecture

### 3.1 Layered model

The project can be represented as the following layered architecture:

```text
Reference / Provenance
        ↓
Reference Rule / Guard
        ↓
Model and Interpretation
        ↓
Observation
        ↓
State x(t)
        ↓
Wave Path
        ↓
V(x), dV/dt
        ↓
Risk
        ↓
Policy
        ↓
Control Command
        ↓
Enforcement Boundary
        ↓
Effect / Observation / Feedback
```

The reference layer is intended to constrain the system rather than become an undocumented source of hidden assumptions. A future implementation can expose the reference trace at decision points through an auditable record.

### 3.2 Reference traceability

The broader Wave Path 2.0 research framework uses concepts such as **reference fingerprint**, **reference guard**, **text wave**, and **effect wave**. In engineering terms, these concepts can be interpreted as traceability mechanisms:

- **Reference fingerprint:** evidence of where a constraint was checked.
- **Reference guard:** a verification barrier between a proposal and execution.
- **Text wave:** an abstract representation of a reference-derived constraint or path; it is not claimed to be a physical wave.
- **Effect wave:** the observed propagation of an action through state and environment.

These are architectural abstractions and must not be confused with physical laws.

---

## 4. Reference Layer and Methodological Boundary

The project's Quran-Core/reference component is treated as a semantic and methodological layer. Selected Qur'anic verses are used within the project's conceptual framework to motivate ideas such as reference, guidance, barriers, effects, and constrained paths. They are **not** used as numerical equations, physical measurements, or substitutes for scientific validation.

Examples retained by the project's research framework include Qur'an 17:45, 17:53, 17:7, 1:6, 59:21, 17:88, and 17:89. Their use in the architecture is interpretive and conceptual; the engineering model remains independently testable.

This separation follows a simple rule:

```text
Reference → interpretation → engineering rule → implementation → test
```

rather than:

```text
Reference → unverified equation → claimed scientific result
```

This distinction is part of the methodology of the paper.

---

## 5. Mathematical Model

### 5.1 Damped-wave model

The integrated experiments use the repository's damped-wave model with configuration:

\[
\omega = 2\pi,
\qquad c = 0.35,
\qquad u_0=1,
\qquad v_0=0.
\]

The exact numerical implementation is the repository source of truth. EXP-012 and EXP-013 use:

- simulation duration: `2.0 s`;
- time step: `0.001 s`;
- angular frequency: `6.283185307179586`;
- damping: `0.35`.

### 5.2 Energy-like quantity

The project computes an oscillator-energy quantity of the form

\[
V(u,v)=\frac{1}{2}v^2+\frac{1}{2}\omega^2u^2.
\]

The manuscript calls this quantity **energy-like** or **Lyapunov-like** because the current experiments use it as a scalar state indicator. A formal Lyapunov stability claim requires explicit system dynamics, equilibrium, domain, positivity conditions, and derivative conditions. A decreasing numerical value in one simulation is not sufficient to establish such a theorem. [4]

### 5.3 Discrete derivative

For consecutive observations,

\[
\frac{dV}{dt}\approx \frac{V_t-V_{t-1}}{t-t_{t-1}}.
\]

The implementation stores both the model derivative and the derivative computed from observed values. This permits direct inspection of model/observation divergence.

### 5.4 Observation model

The observation layer produces:

\[
u_{obs}(t)=u_{model}(t)+\eta(t),
\]

where EXP-013 uses deterministic pseudorandom Gaussian noise with `sigma = 0.01` and `seed = 7`.

The Wave Path calculation in EXP-013 uses the observed displacement rather than silently reverting to the model displacement. This is the key integration change from the zero-noise baseline.

---

## 6. Implementation

The EXP-013 implementation directly imports the repository's:

```text
model.wave.damped_wave
model.observation.observation
lyapunov.lyapunov
wave_path.path
```

The experiment:

1. constructs the wave-model configuration;
2. generates the deterministic wave trajectory;
3. applies controlled deterministic observation noise;
4. calculates observation RMSE;
5. constructs Wave Path points from observed displacement;
6. calculates observed `V` and `dVdt`;
7. records model and observed quantities in CSV;
8. writes a JSON summary;
9. executes structural and numerical validation checks.

The implementation explicitly states that no real network traffic is generated by EXP-013.

---

## 7. Experimental Program

The repository's experimental status document records the following sequence:

| Experiment | Description | Status |
|---|---|---|
| EXP-001 | Integrated synthetic runtime | COMPLETED |
| EXP-002 | Full result analysis | COMPLETED |
| EXP-003 | Wave Path trajectory analysis | COMPLETED |
| EXP-004 | Detection and response analysis | COMPLETED |
| EXP-005 | Result validation | VALIDATED |
| EXP-006 | Sensitivity scenarios | COMPLETED |
| EXP-007 | Sensitivity response/recovery | COMPLETED |
| EXP-008 | Sensitivity validation | VALIDATED |
| EXP-009 | Reproducibility test | REPRODUCIBLE |
| EXP-010 | Final experiment report | COMPLETED |
| EXP-011 | Final integrity audit | VALIDATED |
| EXP-012 | Wave/Observation/Lyapunov/Wave Path integration | VALIDATED |
| EXP-013 | Controlled observation-noise integration | VALIDATED / REPRODUCIBLE |

The status document also explicitly states that the current integrated experiments use synthetic defensive telemetry and do not generate real network or real attack traffic.

---

## 8. Results: EXP-001 to EXP-005

### 8.1 EXP-001

EXP-001 used a synthetic telemetry stream containing 200 events. It reported:

- 200 samples;
- initial `V = 505000.0`;
- final `V = 63419.005`;
- 200 Wave Path points;
- 51 unauthorized events;
- 147 LOW-risk events and 53 HIGH-risk events;
- 147 PASS, 51 OBSERVE_ONLY, and 2 DROP actions.

### 8.2 EXP-002

EXP-002 extended the result stream with `dVdt`, risk, action, and authorization fields. It retained 200 samples and reported minimum `V = 5152.535455565759` and maximum `V = 505000.0`.

### 8.3 EXP-003

EXP-003 reported an `87.44178118811881%` reduction from the initial to final `V` for its synthetic run. The maximum positive `dV/dt` was `176749.99999999985` at `t = 1.50`, while the maximum negative value was `-48480000.0` at `t = 0.01`.

### 8.4 EXP-004

A synthetic disturbance was defined from `t = 1.0` to `t = 1.5`. The first HIGH-risk classification occurred at `1.0`, with simulation-time detection delay `0.0`. The first DROP occurred at `1.58`, producing a simulation-time response delay of `0.58`. Recovery began at `1.67`.

These values are explicitly simulation-time differences. They are not hardware, kernel, network, or production latency measurements.

### 8.5 EXP-005

EXP-005 validated sample count, initial and final `V`, unauthorized-event count, risk counts, and action counts. The recorded validation result is `true`.

---

## 9. Results: EXP-006 to EXP-011

### 9.1 Sensitivity scenarios

EXP-006 evaluated LOW, MEDIUM, and HIGH synthetic disturbance scenarios. Maximum `V` values were:

| Scenario | Maximum V | Maximum dV/dt |
|---|---:|---:|
| LOW | 200.5 | 15000 |
| MEDIUM | 800.5 | 75000 |
| HIGH | 2450.5 | 240000 |

The repository explicitly warns that EXP-006 is a **separate simplified sensitivity model** and is not identical to the exact dynamics of EXP-001. Therefore these numbers must not be merged with EXP-001--EXP-005 as if all experiments used one identical dynamical model.

### 9.2 EXP-007

EXP-007 evaluated scenario-specific disturbance windows and response/recovery behavior. LOW, MEDIUM, and HIGH scenarios were evaluated independently. The reported values are simulation-model outputs, not field measurements.

### 9.3 EXP-008

EXP-008 validated the sensitivity artifacts, including file existence, sample counts, scenario count, finite numeric values, expected `V` ordering, expected `dV/dt` ordering, and scenario maxima. The recorded validation result is `true`.

### 9.4 EXP-009

EXP-009 reran the sensitivity experiment. The SHA-256 output hash before and after rerun was identical:

```text
b602fdf2a8307ec5b8f692a7a27b9cda8cb55f73fdf1b2375a849128569e51f0
```

This establishes reproducibility for that sensitivity experiment under the same software and synthetic-input conditions.

### 9.5 EXP-010 and EXP-011

EXP-010 consolidated the preceding experimental results and limitations. EXP-011 audited the presence and integrity of the principal experimental artifacts and recorded `validation_passed = true`.

---

## 10. EXP-012: Deterministic Integration Baseline

EXP-012 integrates:

```text
Damped Wave Model
        ↓
Observation Layer
        ↓
Lyapunov Calculation
        ↓
Wave Path
```

Its configuration is the same 2.0 s / 0.001 s / `omega = 2π` / damping `0.35` configuration used by EXP-013, but with zero observation noise.

Recorded results:

| Metric | EXP-012 |
|---|---:|
| Samples | 2001 |
| Observation RMSE | 0.0 |
| Maximum absolute noise | 0.0 |
| Initial V | 19.739208802178716 |
| Final V | 4.856389916632241 |
| Minimum V | 4.856389916632241 |
| Maximum V | 19.739208802178716 |
| Wave Path points | 2001 |
| Path displacement | 0.5069535801926761 |
| Maximum V model difference | 0.0 |
| Validation | true |

EXP-012 therefore provides the deterministic integration baseline for EXP-013. The repository explicitly states that EXP-012 does not establish real-world measurement performance, real eBPF/XDP latency, or formal Lyapunov stability.

---

## 11. EXP-013: Controlled Observation-Noise Integration

### 11.1 Objective

EXP-013 extends EXP-012 by introducing controlled observation noise while retaining the actual repository wave model, observation layer, Lyapunov calculation, and Wave Path trajectory.

The experiment's source code explicitly records:

```text
sigma = 0.01
seed = 7
seconds = 2.0
dt = 0.001
omega = 2*pi
damping = 0.35
u0 = 1.0
v0 = 0.0
```

### 11.2 Sample and observation results

The experiment produced 2,001 samples. The observation layer produced:

| Metric | EXP-013 result |
|---|---:|
| Sigma | 0.01 |
| Seed | 7 |
| Observation RMSE | 0.010126179713664026 |
| Maximum absolute noise | 0.03444705105326818 |
| Samples | 2001 |

The positive RMSE and non-zero maximum noise satisfy the experiment's explicit `rmse_positive` and `noise_present` validation checks.

### 11.3 Energy-like results

The observed-state `V` values are:

| Metric | Result |
|---|---:|
| Initial V | 19.638320555259053 |
| Final V | 4.759952605748658 |
| Minimum V | 4.3793514684534065 |
| Maximum V | 20.385783783522392 |
| Maximum V model difference | 0.9140689456240736 |

The final `V` is lower than the initial value for this run, but the maximum exceeds the initial value. Therefore the trajectory is not described here as a proof of monotone Lyapunov decay. The result demonstrates a finite and traceable response of the observed-state calculation to the configured noise.

### 11.4 Wave Path results

EXP-013 generated:

- 2,001 Wave Path points;
- path displacement `0.5093315072746865`;
- monotonic time ordering.

The CSV artifact stores, for each sample, model displacement, observed displacement, velocity, model `V`, observed `V`, model `dV/dt`, observed `dV/dt`, and injected noise.

### 11.5 Validation

The experiment records all of the following as true:

```text
sample_count_correct = true
noise_present = true
rmse_positive = true
wave_path_points_correct = true
finite_values = true
validation_passed = true
```

The status document records repeated execution with seed `7` as producing identical results and classifies EXP-013 as:

```text
VALIDATED / REPRODUCIBLE
```

### 11.6 Scientific interpretation

EXP-013 demonstrates that the integrated software path remains structurally valid when the state used by the Wave Path and energy calculation is derived from a controlled noisy observation rather than the exact model value.

The experiment does **not** provide a universal noise tolerance, robustness guarantee, or field measurement claim. Such claims require parameter sweeps, multiple seeds, alternative noise distributions, missing observations, sampling-rate changes, and eventually realistic data.

---

## 12. Policy and Controller Integration

The project separates analytical policy intent from operational enforcement. Conceptually:

```text
State / V / dVdt / anomaly
            ↓
      Risk classification
            ↓
       Policy decision
            ↓
      Control command
            ↓
   Authorization / guard
            ↓
        Enforcement
```

The policy/controller tests on the integration branch are intended to preserve this separation. A policy can request mitigation while an authorization guard determines whether the requested enforcement action is permitted.

This separation is important for auditability because the following questions remain distinct:

1. What did the analytical layer classify?
2. What did the policy request?
3. What operational command was produced?
4. What did the authorization guard permit?
5. What action was ultimately enforced?

The current policy behavior is an implementation choice, not a universal security policy. In particular, the experimental status document records that an unauthorized event may result in `OBSERVE_ONLY` even when the risk is HIGH.

---

## 13. eBPF/XDP Enforcement Boundary

eBPF provides a kernel-resident programmable execution mechanism with verifier-enforced safety constraints and multiple program types; eBPF maps can provide communication and state-sharing mechanisms between kernel-side programs and userspace. XDP is a high-performance programmable packet-processing path in the Linux networking stack. [1--3]

The Wave Path architecture places eBPF/XDP at the intended low-level enforcement boundary:

```text
Observation / analysis / policy
             ↓
       Control command
             ↓
       eBPF/XDP boundary
             ↓
   packet / event enforcement
```

However, the present experiment series has **not** established an end-to-end kernel benchmark. No numerical latency in EXP-001--EXP-013 should be described as eBPF/XDP latency.

The published XDP literature contains independent performance measurements, but those measurements belong to the XDP system and its experimental setup, not to Wave Path 2.0. [2]

---

## 14. Reproducibility and Artifact Provenance

The central artifacts for the current integrated stage include:

```text
experiments/integrated/results.csv
experiments/integrated/results_full.csv
experiments/integrated/sensitivity_scenarios.csv
experiments/integrated/sensitivity_scenarios.json
experiments/integrated/sensitivity_analysis.json
experiments/integrated/EXP_008_validation.json
experiments/integrated/EXP_010_final_report.json
experiments/integrated/EXP_011_integrity_audit.json
experiments/integrated/EXP_012_wave_observation.py
experiments/integrated/EXP_012_wave_observation.csv
experiments/integrated/EXP_012_wave_observation.json
experiments/integrated/EXP_013_controlled_observation_noise.py
experiments/integrated/EXP_013_controlled_observation_noise.csv
experiments/integrated/EXP_013_controlled_observation_noise.json
tests/test_controller_integration.py
tests/test_policy_integration.py
```

The EXP-013 JSON artifact records configuration, observation metrics, energy-like metrics, Wave Path metrics, and validation flags. The CSV is the sample-level record.

The current repository state has also been checked with the Python test suite; the tested branch reported:

```text
19 passed
```

That result is a software test-suite result. It is not a security benchmark, formal verification result, or field-performance measurement.

---

## 15. Threats to Validity and Limitations

### 15.1 Synthetic data

The integrated experiments use synthetic telemetry. They do not constitute measurements from a real production network or real attack traffic.

### 15.2 No live eBPF/XDP benchmark

The current experimental record does not establish kernel-level performance. In particular, values such as `0.1 ms`, `0.38 ms`, or similar figures must not be presented as experimentally demonstrated performance of this synthetic pipeline.

### 15.3 Lyapunov interpretation

The current `V` is an energy-like / Lyapunov-like quantity. Numerical decrease is not, by itself, a formal stability proof. A formal proof requires explicit mathematical assumptions and conditions. [4]

### 15.4 Rule-based risk model

The current risk classifier is rule-based. No machine-learning detection accuracy is claimed by the experiments.

### 15.5 Simulation timing

Detection and response delays in EXP-004 and related experiments are differences between simulation timestamps. They are not CPU, NIC, kernel, or production response times.

### 15.6 Simplified sensitivity model

EXP-006--EXP-009 use a simplified sensitivity model. Their numerical values must not be treated as if they were produced by exactly the same dynamics as EXP-001--EXP-005.

### 15.7 Reproducibility scope

EXP-009 and EXP-013 demonstrate reproducibility under specified software and synthetic-input conditions. This does not automatically establish bit-for-bit reproducibility across different hardware, operating systems, kernels, compilers, or floating-point environments.

### 15.8 Reference-layer limitation

The reference/Quran-Core layer is a conceptual and semantic layer. It is not a substitute for empirical testing, mathematical proof, or independent engineering validation.

---

## 16. Future Experimental Program

The repository identifies the next boundary as:

```text
Robustness analysis
        ↓
Interface validation
        ↓
Controlled eBPF/XDP integration
        ↓
Benchmarking
```

A rigorous next phase should include:

### 16.1 Robustness

- multiple noise amplitudes;
- multiple deterministic seeds;
- Gaussian and non-Gaussian noise;
- missing observations;
- sampling-rate changes;
- model-parameter perturbations.

### 16.2 Interface validation

Validate the actual interfaces among state, policy, controller, telemetry, and Wave Path, including invalid inputs and failure paths.

### 16.3 eBPF/XDP integration

Use a specified Linux kernel, compiler/LLVM toolchain, loader, network interface, and workload. Record exact versions and configurations.

### 16.4 Benchmarking

Measure separately:

1. packet-processing time;
2. observation overhead;
3. state calculation time;
4. policy decision time;
5. control-command generation;
6. enforcement time;
7. end-to-end latency;
8. throughput;
9. CPU utilization;
10. packet loss/drop behavior.

### 16.5 Formal stability analysis

For a formal Lyapunov result, specify the complete state vector, dynamics, equilibrium, candidate function, domain, and derivative conditions. The proof should be independent of the observation that `V` decreased in a finite simulation.

---

## 17. Claim Classification

To prevent overstatement, every result in future revisions should carry one of these labels:

| Label | Meaning |
|---|---|
| **Measured** | Directly produced by an executed experiment or benchmark |
| **Derived** | Calculated from measured or stored experimental values |
| **Model assumption** | Defined by the mathematical or software model |
| **Proposed** | Architectural idea or future experiment |
| **Not established** | A claim that the current evidence does not support |

For the current manuscript, EXP-013 numerical values are **Measured** within a synthetic software experiment. The interpretation that the system is formally stable is **Not established**.

---

## 18. Conclusion

Wave Path 2.0 currently provides a reproducible synthetic reference implementation for an observation-driven control architecture connecting state representation, an energy-like Lyapunov quantity, derivative estimation, risk classification, policy intent, operational control, authorization, and Wave Path trajectory recording.

The progression from EXP-012 to EXP-013 is the principal new experimental step. EXP-012 established deterministic zero-noise integration. EXP-013 introduced controlled Gaussian observation noise with `sigma = 0.01` and seed `7`, generated 2,001 samples and 2,001 Wave Path points, produced positive observation RMSE and non-zero injected noise, preserved finite numerical values, and passed all programmed validation checks. The repository records repeated execution with the same seed as identical.

Taken together, EXP-001--EXP-013 support the narrower conclusion that the repository contains a functioning and traceable **synthetic integrated experimental layer** with validation and reproducibility artifacts. They do not establish real-world security performance, production-network behavior, real eBPF/XDP latency, zero-exfiltration guarantees, AI detection performance, or a formal Lyapunov-stability theorem.

The research boundary is therefore explicit: move next from synthetic robustness to interface validation, then to controlled kernel integration and benchmarked measurements. Any stronger claim should be introduced only after the corresponding experiment or proof exists in the repository.

---

## References

1. Linux Kernel Documentation, **BPF Documentation**, including eBPF verifier, maps, program types, and userspace interaction. https://www.kernel.org/doc/html/latest/bpf/

2. T. Høiland-Jørgensen, J. D. Brouer, D. Borkmann, J. Fastabend, T. Herbert, D. Ahern, and D. Miller, “The eXpress Data Path: Fast Programmable Packet Processing in the Operating System Kernel,” *ACM CoNEXT 2018*, DOI: 10.1145/3281411.3281443. https://doi.org/10.1145/3281411.3281443

3. eBPF Docs, **eBPF on Linux**, including program types, verifier, maps, and kernel/userspace interaction. https://docs.ebpf.io/linux/

4. H. K. Khalil, *Nonlinear Systems*, 3rd ed., Prentice Hall/Pearson, 2002. Chapter 4 covers Lyapunov stability and related nonlinear-systems analysis.

5. Wave Path 2.0 repository, `wave-path-2-integration`, including integrated experiment artifacts, controller/policy tests, and source implementation.

---

## Data and Code Availability

The code and experimental artifacts are maintained in the Wave Path 2.0 repository. The `wave-path-2-integration` branch contains the integrated experiment scripts, persistent CSV/JSON artifacts, controller/policy integration tests, and this manuscript.

For reproducibility, a publication submission should identify the exact repository commit used to generate every reported table and figure. The manuscript should not be detached from its corresponding artifact set.

---

## Scientific Status

This document is a **research/reproducibility manuscript**, not a statement of peer review. External peer review, independent replication, and any required venue-specific validation remain separate stages.
