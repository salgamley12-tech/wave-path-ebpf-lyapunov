#!/usr/bin/env bash
set -e

cd ~/wave-path-ebpf-lyapunov

echo "[*] Step 1: Purging all local and global cargo configurations..."
cargo clean 2>/dev/null || true
rm -rf Cargo.lock .cargo target/
rm -f ~/.cargo/config.toml

echo "[*] Step 2: Sanitizing root Cargo.toml from any forced target..."
python3 -c '
import pathlib, re
path = pathlib.Path("Cargo.toml")
if path.exists():
    content = path.read_text("utf-8")
    # إزالة أي قسم workspace أو target قديم
    content = re.sub(r"\[workspace\].*?(?=\n\[|\Z)", "", content, flags=re.DOTALL)
    content = re.sub(r"target\s*=.*", "", content)
    path.write_text(content, "utf-8")
    print("[+] Cargo.toml sanitized successfully.")
'

echo "[*] Step 3: Detecting native host target..."
HOST_TARGET=$(rustc -vV | grep "host:" | awk '{print $2}')
echo "[+] Target architecture detected: $HOST_TARGET"

echo "[*] Step 4: Building user-space daemon explicitly for native host..."
# بناء الديمون قسراً على معمارية هاتفك الحقيقية وببيئة std الكاملة
/data/data/com.termux/files/usr/bin/cargo build --release --target "$HOST_TARGET"

echo "[SUCCESS] Build completed successfully!"

# تشغيل الديمون فوراً
if [ -f "./target/$HOST_TARGET/release/wave-path-daemon" ]; then
    ./target/$HOST_TARGET/release/wave-path-daemon
elif [ -f "./target/release/wave-path-daemon" ]; then
    ./target/release/wave-path-daemon
else
    /data/data/com.termux/files/usr/bin/cargo run --release
fi
