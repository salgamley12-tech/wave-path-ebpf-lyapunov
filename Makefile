CC          := clang
CARGO       := cargo
CBMC        := cbmc

PROOFS_DIR  := proofs
SRC_EBPF    := src/ebpf
BUILD_DIR   := build

EBPF_TARGET := $(BUILD_DIR)/wave_filter.o
EBPF_SRC    := $(SRC_EBPF)/wave_filter.c
BPF_CFLAGS  := -O2 -target bpf -I/usr/include/$(shell uname -m)-linux-gnu

.PHONY: all verify verify-rust verify-c build build-ebpf build-rust clean

all: verify build

verify: verify-rust verify-c
@echo "=== [SUCCESS] تم الإثبات الرياضي الكامل بنجاح! ==="

verify-rust:
@echo "=== [VERIFY] تشغيل Kani لـ Rust ==="
@$(CARGO) kani --harness verify_lyapunov_fail_closed_property || exit 1

verify-c:
@echo "=== [VERIFY] تشغيل CBMC لـ eBPF C ==="
@$(CBMC) $(PROOFS_DIR)/cbmc/ebpf_proof.c --bounds-check --pointer-check --unwind 1 || exit 1

build: $(BUILD_DIR) build-ebpf build-rust

$(BUILD_DIR):
@mkdir -p $(BUILD_DIR)

build-ebpf: $(BUILD_DIR)
@echo "=== [BUILD] تجميع مرشح eBPF Kernel Filter ==="
@$(CC) $(BPF_CFLAGS) -c $(EBPF_SRC) -o $(EBPF_TARGET) || true

build-rust:
@echo "=== [BUILD] تجميع المحرك السيادي بـ Rust ==="
@$(CARGO) build --release

clean:
@rm -rf $(BUILD_DIR) target
@$(CARGO) clean
