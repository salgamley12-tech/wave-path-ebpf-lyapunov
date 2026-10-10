#!/usr/bin/env bash
set -e

cd ~/wave-path-ebpf-lyapunov

echo "[*] Step 1: Temporarily moving eBPF kernel folder to safe home directory..."
mkdir -p ~/ebpf_safe_backup
for d in */; do
    d_name="${d%/}"
    if [ -f "${d}Cargo.toml" ] && (grep -q "bpf" "${d}Cargo.toml" || grep -q "ebpf" "${d}Cargo.toml" || [ "$d_name" = "ebpf" ]); then
        mv "$d_name" ~/ebpf_safe_backup/
        echo "[+] Isolated kernel folder: $d_name"
    fi
done

echo "[*] Step 2: Purging all caches, locks, and configurations..."
cargo clean 2>/dev/null || true
rm -rf Cargo.lock .cargo target/

echo "[*] Step 3: Building daemon in pure std environment without any interference..."
/data/data/com.termux/files/usr/bin/cargo build --release

echo "[SUCCESS] Daemon built successfully!"

echo "[*] Step 4: Restoring eBPF kernel folder back to project..."
cp -r ~/ebpf_safe_backup/* ./ 2>/dev/null || true
rm -rf ~/ebpf_safe_backup

echo "[*] Step 5: Launching daemon..."
if [ -f "./target/release/wave-path-daemon" ]; then
    ./target/release/wave-path-daemon
elif [ -f "./target/release/wave_path_daemon" ]; then
    ./target/release/wave_path_daemon
else
    /data/data/com.termux/files/usr/bin/cargo run --release
fi
