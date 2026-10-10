#!/usr/bin/env bash
set -e

# 1. تفعيل مسار أدوات النايتلي والتوجه للمجلد
export PATH="$HOME/.local-rust/bin:$PATH"
cd ~/wave-path-ebpf-lyapunov

echo "[*] Step 1: Cleaning workspace and removing leaked global configs..."
cargo clean 2>/dev/null || true
rm -rf Cargo.lock .cargo/

# 2. البحث الآلي عن مجلد النواة الفرعي (eBPF)
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

# 3. بناء النواة بمعزل تام وتخصيص إعداداتها داخل مجلدها الفرعي فقط
if [ -n "$EBPF_DIR" ]; then
    echo "[*] Step 2: Configuring and building eBPF kernel independently..."
    mkdir -p "${EBPF_DIR}/.cargo"
    cat << 'CONFIG_EOF' > "${EBPF_DIR}/.cargo/config.toml"
[build]
target = "bpfel-unknown-none"

[unstable]
build-std = ["core"]
CONFIG_EOF

    cargo build --manifest-path "${EBPF_DIR}/Cargo.toml" --target bpfel-unknown-none -Z build-std=core --release
fi

# 4. بناء الديمون (User-space Daemon) ببيئة std القياسية الكاملة وبدون أي قيود أو تسريب
echo "[*] Step 3: Building user-space daemon (wave-path-daemon)..."
cargo build --release --bin wave-path-daemon

echo "[SUCCESS] Build pipeline completed successfully!"

# 5. التشغيل الفوري للديمون
if [ -f "./target/release/wave-path-daemon" ]; then
    echo "[+] Launching wave-path-daemon..."
    ./target/release/wave-path-daemon
else
    echo "[-] Checking alternative binary paths..."
    cargo run --release --bin wave-path-daemon
fi
