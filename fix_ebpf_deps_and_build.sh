#!/usr/bin/env bash
set -e

cd ~/wave-path-ebpf-lyapunov

echo "[*] Step 1: Locating eBPF kernel directory..."
EBPF_DIR=""
for d in */; do
    if [ -f "${d}Cargo.toml" ]; then
        if grep -q "bpf" "${d}Cargo.toml" || grep -q "ebpf" "${d}Cargo.toml" || [ "${d%/}" = "ebpf" ]; then
            EBPF_DIR="${d%/}"
            break
        fi
    fi
done

echo "[+] Detected eBPF directory: ${EBPF_DIR}"

# الخطوة 2: تنظيف ملف Cargo.toml الخاص بالنواة من أي اعتماد على anyhow أو std crates
if [ -n "$EBPF_DIR" ] && [ -f "${EBPF_DIR}/Cargo.toml" ]; then
    echo "[*] Step 2: Purging any illegal std dependencies (like anyhow) from eBPF crate..."
    python3 -c '
import pathlib
path = pathlib.Path("'${EBPF_DIR}'/Cargo.toml")
content = path.read_text("utf-8")
# إزالة anyhow أو مكتبات الـ std إن وجدت بالخطأ في قسم الاعتمادات الخاص بالنواة
lines = content.splitlines()
new_lines = []
skip = False
for line in lines:
    if "anyhow" in line or "std" in line and "no_std" not in line:
        print(f"[-] Removing illegal line from eBPF Cargo.toml: {line}")
        continue
    new_lines.append(line)
path.write_text("\n".join(new_lines), "utf-8")
'
fi

echo "[*] Step 3: Cleaning cargo cache..."
/data/data/com.termux/files/usr/bin/cargo clean 2>/dev/null || true
rm -rf .cargo/ Cargo.lock target/

echo "[*] Step 4: Building user-space daemon cleanly using Termux stable Cargo..."
# بناء الديمون الخاص بالفضاء المستخدم حصرياً باستخدام مترجم ترمكس الرسمي
/data/data/com.termux/files/usr/bin/cargo build --release --bin wave-path-daemon

echo "[SUCCESS] Build completed successfully!"

# الخطوة 5: التشغيل الفوري للنظام
if [ -f "./target/release/wave-path-daemon" ]; then
    echo "[+] Launching wave-path-daemon..."
    ./target/release/wave-path-daemon
else
    /data/data/com.termux/files/usr/bin/cargo run --release --bin wave-path-daemon
fi
