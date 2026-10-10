#!/usr/bin/env bash
set -e

cd ~/wave-path-ebpf-lyapunov

echo "[*] Step 1: Purging all .cargo directories and build artifacts across the project..."
rm -rf .cargo/ target/ target-ebpf/ Cargo.lock
find . -type d -name ".cargo" -exec rm -rf {} + 2>/dev/null || true

echo "[*] Step 2: Uncoupling workspace in root Cargo.toml to prevent target leakage..."
python3 -c '
import re
if __import__("os").path.exists("Cargo.toml"):
    with open("Cargo.toml", "r", encoding="utf-8") as f:
        content = f.read()
    # إزالة قسم workspace تماماً من الجذر لمنع التداخل
    content = re.sub(r"\[workspace\]\s*(?:\n\w+\s*=\s*\[.*?\])*", "", content, flags=re.DOTALL)
    with open("Cargo.toml", "w", encoding="utf-8") as f:
        f.write(content)
'

echo "[*] Step 3: Detecting eBPF kernel directory..."
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

echo "[+] Detected eBPF folder: ${EBPF_DIR}"

# 4. بناء النواة وحدها بملف config خاص به داخل مجلدها فقط مع توجيه المخرجات للخارج
if [ -n "$EBPF_DIR" ]; then
    mkdir -p "${EBPF_DIR}/.cargo"
    cat << 'CFG' > "${EBPF_DIR}/.cargo/config.toml"
[build]
target = "bpfel-unknown-none"

[unstable]
build-std = ["core"]
CFG

    echo "[*] Compiling eBPF kernel with Nightly..."
    "$HOME/.local-rust/bin/cargo" build --manifest-path "${EBPF_DIR}/Cargo.toml" --target bpfel-unknown-none -Z build-std=core --target-dir ../target-ebpf --release
fi

# 5. بناء الديمون (User-space Daemon) باستخدام مترجم ترمكس المستقر ببيئة std الحقيقية والنظيفة
echo "[*] Compiling user-space daemon with Termux stable Cargo..."
/data/data/com.termux/files/usr/bin/cargo build --release --bin wave-path-daemon

echo "[SUCCESS] Build completed successfully with absolute isolation!"

# 6. التشغيل الفوري للنظام
if [ -f "./target/release/wave-path-daemon" ]; then
    echo "[+] Launching wave-path-daemon..."
    ./target/release/wave-path-daemon
else
    /data/data/com.termux/files/usr/bin/cargo run --release --bin wave-path-daemon
fi
