#!/usr/bin/env bash
set -e

# 1. تفعيل أدوات النايتلي والتوجه للمجلد
export PATH="$HOME/.local-rust/bin:$PATH"
cd ~/wave-path-ebpf-lyapunov

echo "[*] Step 1: Purging all global configs and cache..."
cargo clean 2>/dev/null || true
rm -rf .cargo/ Cargo.lock

# 2. العثور على مجلد النواة (eBPF) تلقائياً
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

# 3. بناء النواة بمعزل تام عبر تخصيص ملف الـ config داخل مجلدها الفرعي فقط دون الجذر
if [ -n "$EBPF_DIR" ]; then
    mkdir -p "${EBPF_DIR}/.cargo"
    cat << 'CFG' > "${EBPF_DIR}/.cargo/config.toml"
[build]
target = "bpfel-unknown-none"

[unstable]
build-std = ["core"]
CFG

    echo "[*] Step 2: Compiling eBPF kernel..."
    cargo build --manifest-path "${EBPF_DIR}/Cargo.toml" --target bpfel-unknown-none -Z build-std=core --release
fi

# 4. بناء الفضاء المستخدم والديمون ببيئة std الطبيعية وبدون أي قيود متسربة
echo "[*] Step 3: Compiling user-space daemon..."
cargo build --release

echo "[SUCCESS] Build completed successfully!"

# 5. التشغيل الفوري للنظام
if [ -f "./target/release/wave-path-daemon" ]; then
    ./target/release/wave-path-daemon
else
    cargo run --release
fi
