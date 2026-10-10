#!/usr/bin/env bash
set -e

# تحديد المسارات بدقة مطلقة
SYS_CARGO="/data/data/com.termux/files/usr/bin/cargo"
NIGHTLY_CARGO="$HOME/.local-rust/bin/cargo"

cd ~/wave-path-ebpf-lyapunov

echo "[*] Step 1: Cleaning workspace..."
$SYS_CARGO clean 2>/dev/null || true
rm -rf .cargo/ Cargo.lock

# العثور على مجلد النواة (eBPF) تلقائياً
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

# الخطوة 2: بناء النواة بمعزل تام باستخدام أداة النايتلي حصرياً
if [ -n "$EBPF_DIR" ]; then
    echo "[*] Step 2: Compiling eBPF kernel using Nightly toolchain..."
    mkdir -p "${EBPF_DIR}/.cargo"
    cat << 'CFG' > "${EBPF_DIR}/.cargo/config.toml"
[build]
target = "bpfel-unknown-none"

[unstable]
build-std = ["core"]
CFG

    "$NIGHTLY_CARGO" build --manifest-path "${EBPF_DIR}/Cargo.toml" --target bpfel-unknown-none -Z build-std=core --release
fi

# الخطوة 3: بناء الديمون (User-space Daemon) باستخدام مُعرّف ترمكس المستقر (الذي يمتلك std كاملة)
echo "[*] Step 3: Compiling user-space daemon using Termux Stable Rust..."
$SYS_CARGO build --release --bin wave-path-daemon

echo "[SUCCESS] Build completed successfully with absolute precision!"

# الخطوة 4: الإقلاع الفوري
if [ -f "./target/release/wave-path-daemon" ]; then
    echo "[+] Launching wave-path-daemon..."
    ./target/release/wave-path-daemon
else
    $SYS_CARGO run --release --bin wave-path-daemon
fi
