#!/usr/bin/env bash
set -e

SYS_CARGO="/data/data/com.termux/files/usr/bin/cargo"
NIGHTLY_CARGO="$HOME/.local-rust/bin/cargo"

cd ~/wave-path-ebpf-lyapunov

echo "[*] Cleaning all caches and root configs..."
$SYS_CARGO clean 2>/dev/null || true
rm -rf .cargo/ Cargo.lock target/

# 1. اكتشاف مجلد النواة تلقائياً
EBPF_DIR=""
for d in */; do
    if [ -f "${d}Cargo.toml" ]; then
        if grep -q "bpf" "${d}Cargo.toml" || grep -q "ebpf" "${d}Cargo.toml" || [ "${d%/}" = "ebpf" ]; then
            EBPF_DIR="${d%/}"
            break
        fi
    fi
done

echo "[+] Detected eBPF kernel directory: ${EBPF_DIR}"

# 2. بناء النواة حصرياً داخل مجلدها بملف config خاص بها وبدون تلويث الجذر
if [ -n "$EBPF_DIR" ]; then
    mkdir -p "${EBPF_DIR}/.cargo"
    cat << 'CFG' > "${EBPF_DIR}/.cargo/config.toml"
[build]
target = "bpfel-unknown-none"

[unstable]
build-std = ["core"]
CFG

    echo "[*] Building eBPF kernel with Nightly..."
    "$NIGHTLY_CARGO" build --manifest-path "${EBPF_DIR}/Cargo.toml" --target bpfel-unknown-none -Z build-std=core --release
fi

# 3. بناء الديمون من الجذر باستخدام مستودع ترمكس المستقر (بدون أي config في الجذر ليعمل بشكل طبيعي مع std)
echo "[*] Building user-space daemon with System Cargo..."
$SYS_CARGO build --release --bin wave-path-daemon

echo "[SUCCESS] Build completed successfully!"

# 4. الإقلاع الفوري
if [ -f "./target/release/wave-path-daemon" ]; then
    echo "[+] Launching wave-path-daemon..."
    ./target/release/wave-path-daemon
else
    $SYS_CARGO run --release --bin wave-path-daemon
fi
