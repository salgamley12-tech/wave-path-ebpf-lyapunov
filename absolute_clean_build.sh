#!/usr/bin/env bash
set -e

# 1. تفعيل مسار أدوات النايتلي والتوجه لمجلد المشروع
export PATH="$HOME/.local-rust/bin:$PATH"
cd ~/wave-path-ebpf-lyapunov

echo "[*] Purging all build artifacts and root .cargo pollution..."
cargo clean 2>/dev/null || true
rm -rf .cargo/ target/ Cargo.lock

# 2. التحقق مما إذا كان المشروع يستخدم نظام xtask الخاص بـ Aya (وهو الأسلوب القياسي)
if [ -d "xtask" ]; then
    echo "[+] Detected Aya xtask structure. Building via xtask..."
    # بناء النواة عبر xtask
    cargo xtask build-ebpf --release
    
    echo "[+] Building user-space daemon..."
    cargo build --release --bin wave-path-daemon
    
    echo "[SUCCESS] Build complete! Launching daemon..."
    ./target/release/wave-path-daemon
else
    echo "[+] Standard structure detected. Building eBPF crate isolated..."
    
    # البحث عن مجلد النواة الفرعي وبناؤه بملف config خاص به وحده داخل مجلدها
    for d in */; do
        if [ -f "${d}Cargo.toml" ]; then
            if grep -q "bpf" "${d}Cargo.toml" || grep -q "ebpf" "${d}Cargo.toml" || [ "${d%/}" = "ebpf" ]; then
                echo "[+] Found eBPF crate at: ${d%/}"
                mkdir -p "${d}.cargo"
                cat << 'CFG' > "${d}.cargo/config.toml"
[build]
target = "bpfel-unknown-none"

[unstable]
build-std = ["core"]
CFG
                cargo build --manifest-path "${d}Cargo.toml" --target bpfel-unknown-none -Z build-std=core --release
            fi
        fi
    done

    echo "[+] Building user-space daemon cleanly from root..."
    cargo build --release --bin wave-path-daemon
    
    echo "[SUCCESS] Build complete! Launching daemon..."
    ./target/release/wave-path-daemon
fi
