#!/usr/bin/env bash
set -e

cd ~/wave-path-ebpf-lyapunov

echo "[*] Step 1: Purging leaking environment variables..."
unset CARGO_BUILD_TARGET
unset CARGO_BUILD_STD
unset RUSTFLAGS

echo "[*] Step 2: Removing global cargo configuration pollution in ~/.cargo/..."
rm -f ~/.cargo/config.toml

echo "[*] Step 3: Cleaning local workspace..."
/data/data/com.termux/files/usr/bin/cargo clean 2>/dev/null || true
rm -rf .cargo/ Cargo.lock target/

echo "[*] Step 4: Building user-space daemon cleanly with system Cargo..."
# استخدام مترجم ترمكس الرسمي مباشرة وبدون أي تداخل
/data/data/com.termux/files/usr/bin/cargo build --release --bin wave-path-daemon

echo "[SUCCESS] The daemon has compiled successfully!"

# الإقلاع الفوري
if [ -f "./target/release/wave-path-daemon" ]; then
    echo "[+] Launching wave-path-daemon..."
    ./target/release/wave-path-daemon
else
    /data/data/com.termux/files/usr/bin/cargo run --release --bin wave-path-daemon
fi
