#!/usr/bin/env bash
set -e

cd ~/wave-path-ebpf-lyapunov

echo "[*] Step 1: Cleaning root workspace..."
cargo clean 2>/dev/null || true
rm -rf .cargo/ Cargo.lock target/

echo "[*] Step 2: Locating User-Space Daemon directory..."
DAEMON_DIR=""
for d in */; do
    d_name="${d%/}"
    # البحث عن المجلد الذي ليس ebpf ولا target
    if [ "$d_name" != "ebpf" ] && [ "$d_name" != "target" ] && [ "$d_name" != "target-ebpf" ] && [ -f "${d}Cargo.toml" ]; then
        # التأكد أنه ليس مجلد نواة eBPF
        if ! grep -q "bpf" "${d}Cargo.toml" && ! grep -q "ebpf" "${d}Cargo.toml"; then
            DAEMON_DIR="$d_name"
            break
        fi
    fi
done

if [ -z "$DAEMON_DIR" ]; then
    # إذا لم يُعثر عليه، فلنبحث عن أي مجلد يحتوي على Cargo.toml بخلاف ebpf
    DAEMON_DIR=$(find . -maxdepth 2 -name "Cargo.toml" ! -path "./Cargo.toml" ! -path "*/ebpf/*" -exec dirname {} \; | head -n 1 | sed 's|^\./||')
fi

echo "[+] Detected Daemon directory: ${DAEMON_DIR}"

if [ -n "$DAEMON_DIR" ] && [ -d "$DAEMON_DIR" ]; then
    cd "$DAEMON_DIR"
    echo "[*] Step 3: Isolating daemon and building independently with Termux stable Cargo..."
    rm -rf .cargo/ Cargo.lock target/
    
    # بناء الديمون حصرياً ببيئة std القياسية
    /data/data/com.termux/files/usr/bin/cargo build --release
    
    echo "[SUCCESS] Daemon built successfully!"
    
    # محاولة التشغيل
    if [ -f "target/release/wave-path-daemon" ]; then
        ./target/release/wave-path-daemon
    elif [ -f "target/release/wave_path_daemon" ]; then
        ./target/release/wave_path_daemon
    else
        /data/data/com.termux/files/usr/bin/cargo run --release
    fi
else
    echo "[-] Could not isolate daemon directory automatically. Please specify the folder name."
fi
