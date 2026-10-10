#!/usr/bin/env bash
set -e

SYS_CARGO="/data/data/com.termux/files/usr/bin/cargo"
NIGHTLY_CARGO="$HOME/.local-rust/bin/cargo"

cd ~/wave-path-ebpf-lyapunov

echo "[*] Step 1: Cleaning everything and removing global cargo configs..."
$SYS_CARGO clean 2>/dev/null || true
rm -rf .cargo/ Cargo.lock

# 2. فك ارتباط مساحة العمل (Workspace) في ملف Cargo.toml الرئيسي لمنع أي تداخل
python3 -c '
with open("Cargo.toml", "r", encoding="utf-8") as f:
    content = f.read()

if "[workspace]" in content:
    print("[+] Breaking workspace coupling in root Cargo.toml...")
    import re
    content = re.sub(r"\[workspace\]\s*(?:\n\w+\s*=\s*\[.*?\])*", "", content, flags=re.DOTALL)
    with open("Cargo.toml", "w", encoding="utf-8") as fw:
        fw.write(content)
'

# 3. العثور على مجلد النواة (eBPF)
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

# 4. بناء النواة وحدها تماماً داخل مجلدها باستخدام النايتلي
if [ -n "$EBPF_DIR" ]; then
    echo "[*] Step 2: Building eBPF kernel independently..."
    mkdir -p "${EBPF_DIR}/.cargo"
    cat << 'CFG' > "${EBPF_DIR}/.cargo/config.toml"
[build]
target = "bpfel-unknown-none"

[unstable]
build-std = ["core"]
CFG

    "$NIGHTLY_CARGO" build --manifest-path "${EBPF_DIR}/Cargo.toml" --target bpfel-unknown-none -Z build-std=core --release
fi

# 5. بناء الديمون حصرياً باستخدام مستودع ترمكس المستقر وبشكل منفصل تماماً
echo "[*] Step 3: Building user-space daemon cleanly with system Cargo..."
$SYS_CARGO build --release --bin wave-path_daemon 2>/dev/null || $SYS_CARGO build --release --bin wave-path-daemon

echo "[SUCCESS] Build completed successfully without any workspace interference!"

# 6. التشغيل الفوري
if [ -f "./target/release/wave-path-daemon" ]; then
    ./target/release/wave-path-daemon
elif [ -f "./target/release/wave-path_daemon" ]; then
    ./target/release/wave-path_daemon
else
    $SYS_CARGO run --release
fi
