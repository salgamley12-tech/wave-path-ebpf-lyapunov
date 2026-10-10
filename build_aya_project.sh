#!/usr/bin/env bash
set -e

cd ~/wave-path-ebpf-lyapunov

echo "[*] Step 1: Cleaning workspace artifacts..."
/data/data/com.termux/files/usr/bin/cargo clean 2>/dev/null || true
rm -rf target/ target-ebpf/ Cargo.lock

# 2. البحث عن مجلد النواة الفرعي (eBPF)
EBPF_DIR=""
for d in */; do
    d_name="${d%/}"
    if [ -f "${d}Cargo.toml" ]; then
        if grep -q "bpf" "${d}Cargo.toml" || grep -q "ebpf" "${d}Cargo.toml" || [ "$d_name" = "ebpf" ]; then
            EBPF_DIR="$d_name"
            break
        fi
    fi
done

echo "[+] Detected eBPF kernel directory: ${EBPF_DIR}"

# 3. بناء النواة بمعزل تام داخل مجلدها باستخدام النايتلي
if [ -n "$EBPF_DIR" ]; then
    mkdir -p "${EBPF_DIR}/.cargo"
    cat << 'CFG' > "${EBPF_DIR}/.cargo/config.toml"
[build]
target = "bpfel-unknown-none"

[unstable]
build-std = ["core"]
CFG

    echo "[*] Building eBPF kernel..."
    "$HOME/.local-rust/bin/cargo" build --manifest-path "${EBPF_DIR}/Cargo.toml" --target bpfel-unknown-none -Z build-std=core --target-dir ../target-ebpf --release
fi

# 4. بناء الديمون من المجلد الرئيسي (Root) باستخدام مترجم ترمكس المستقر ببيئة std الطبيعية
echo "[*] Building user-space daemon from root directory..."
/data/data/com.termux/files/usr/bin/cargo build --release

echo "[SUCCESS] Build finished successfully!"

# 5. التشغيل الفوري للنظام
if [ -f "./target/release/wave-path-daemon" ]; then
    echo "[+] Launching wave-path-daemon..."
    ./target/release/wave-path-daemon
elif [ -f "./target/release/wave_path_daemon" ]; then
    echo "[+] Launching wave_path_daemon..."
    ./target/release/wave_path_daemon
else
    /data/data/com.termux/files/usr/bin/cargo run --release
fi
