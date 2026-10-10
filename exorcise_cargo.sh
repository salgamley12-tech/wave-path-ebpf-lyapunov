#!/usr/bin/env bash
set -e

export PATH="$HOME/.local-rust/bin:$PATH"
cd ~/wave-path-ebpf-lyapunov

echo "[*] Exorcising cargo ghosts: purging all global .cargo/ and target/..."
cargo clean 2>/dev/null || true
rm -rf .cargo/ Cargo.lock

# 1. البحث عن مجلد النواة بدقة
EBPF_DIR=""
for d in */; do
    if [ -f "${d}Cargo.toml" ]; then
        if grep -q "bpf" "${d}Cargo.toml" || grep -q "ebpf" "${d}Cargo.toml" || [ "${d%/}" = "ebpf" ]; then
            EBPF_DIR="${d%/}"
            break
        fi
    fi
done

echo "[+] Target eBPF folder: ${EBPF_DIR}"

# 2. بناء النواة وحدها بداخل مجلدها الفرعي حصرياً ودون أي تأثير على الجذر
if [ -n "$EBPF_DIR" ]; then
    mkdir -p "${EBPF_DIR}/.cargo"
    cat << 'CFG' > "${EBPF_DIR}/.cargo/config.toml"
[build]
target = "bpfel-unknown-none"

[unstable]
build-std = ["core"]
CFG

    echo "[*] Building sovereign eBPF kernel..."
    cargo build --manifest-path "${EBPF_DIR}/Cargo.toml" --target bpfel-unknown-none -Z build-std=core --release
fi

# 3. بناء الديمون في مساحة المستخدم ببيئة std الحقيقية والنظيفة 100%
echo "[*] Building wave-path-daemon in standard user-space..."
cargo build --release --bin wave-path-daemon

echo "[SUCCESS] The daemon is clean and ready!"

# 4. التشغيل الفوري
if [ -f "./target/release/wave-path-daemon" ]; then
    ./target/release/wave-path-daemon
else
    cargo run --release --bin wave-path-daemon
fi
