#!/usr/bin/env bash
set -e

cd ~/wave-path-ebpf-lyapunov

echo "[*] Step 1: Moving root .cargo config to its correct place inside ebpf folder..."
if [ -f ".cargo/config.toml" ]; then
    mkdir -p ebpf/.cargo
    mv .cargo/config.toml ebpf/.cargo/config.toml
    rm -rf .cargo
    echo "[+] Root .cargo/config.toml successfully relocated to ebpf/.cargo/config.toml"
fi

echo "[*] Step 2: Sanitizing root Cargo.toml workspace settings..."
python3 -c '
import pathlib, re
path = pathlib.Path("Cargo.toml")
if path.exists():
    content = path.read_text("utf-8")
    # إزالة أي فرض للـ target من الجذر
    content = re.sub(r"^\s*target\s*=.*$", "", content, flags=re.MULTILINE)
    path.write_text(content, "utf-8")
    print("[+] Root Cargo.toml sanitized.")
'

echo "[*] Step 3: Cleaning all cache and lock files..."
cargo clean
rm -rf Cargo.lock

echo "[*] Step 4: Detecting host target and building daemon in pure std environment..."
HOST_TARGET=$(rustc -vV | grep "host:" | awk '{print $2}')
echo "[+] Host Target: $HOST_TARGET"

# بناء الديمون حصرياً باستخدام هدف النظام القياسي متخطياً النواة بالكامل
/data/data/com.termux/files/usr/bin/cargo build --release --target "$HOST_TARGET"

echo "[SUCCESS] wave-path-daemon built successfully!"

echo "[*] Step 5: Launching daemon..."
if [ -f "./target/$HOST_TARGET/release/wave-path-daemon" ]; then
    ./target/$HOST_TARGET/release/wave-path-daemon
elif [ -f "./target/release/wave-path-daemon" ]; then
    ./target/release/wave-path-daemon
else
    /data/data/com.termux/files/usr/bin/cargo run --release
fi
