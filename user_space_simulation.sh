#!/usr/bin/env bash
set -e

cd ~/wave-path-ebpf-lyapunov

echo "[*] Step 1: Converting project to pure user-space standard mode..."

# تنظيف كافة مخلفات البناء السابقة وملفات التكوين المعزولة
cargo clean 2>/dev/null || true
rm -rf .cargo/ Cargo.lock target/ target-ebpf/
find . -name "config.toml" -delete

# 2. تعديل ملف Cargo.toml الرئيسي لإلغاء أي ارتباط بـ workspace أو نواة الـ eBPF
python3 -c '
import pathlib, re
path = pathlib.Path("Cargo.toml")
if path.exists():
    content = path.read_text("utf-8")
    # إزالة قسم workspace تماماً لمنع فرض تداخل الأهداف
    content = re.sub(r"\[workspace\]\s*(?:\n\w+\s*=\s*\[.*?\])*", "", content, flags=re.DOTALL)
    path.write_text(content, "utf-8")
    print("[+] Root Cargo.toml uncoupled successfully.")
'

# 3. بناء الفضاء المستخدم حصرياً باستخدام مترجم ترمكس المستقر (بيئة std القياسية)
echo "[*] Step 2: Building daemon in pure std environment..."
/data/data/com.termux/files/usr/bin/cargo build --release

echo "[SUCCESS] The daemon has been built successfully in user-space mode!"

# 4. التشغيل الفوري للنظام
if [ -f "./target/release/wave-path-daemon" ]; then
    echo "[+] Launching wave-path-daemon..."
    ./target/release/wave-path-daemon
elif [ -f "./target/release/wave_path_daemon" ]; then
    echo "[+] Launching wave_path_daemon..."
    ./target/release/wave_path_daemon
else
    /data/data/com.termux/files/usr/bin/cargo run --release
fi
