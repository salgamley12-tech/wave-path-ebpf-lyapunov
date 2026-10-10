#!/usr/bin/env bash
set -e

cd ~/wave-path-ebpf-lyapunov

echo "[*] Step 1: Purging EVERY single config.toml file across all subdirectories..."
find . -name "config.toml" -print -delete

echo "[*] Step 2: Cleaning all build caches..."
cargo clean 2>/dev/null || true
rm -rf Cargo.lock target/ target-ebpf/

echo "[*] Step 3: Analyzing Cargo.toml structure and package names..."
python3 -c '
import os, re

ebpf_pkg = None
daemon_pkg = None

for root, dirs, files in os.walk("."):
    if "Cargo.toml" in files and "target" not in root:
        path = os.path.join(root, "Cargo.toml")
        content = open(path, "r", encoding="utf-8").read()
        name_match = re.search(r"name\s*=\s*\"([^\"]+)\"", content)
        if name_match:
            name = name_match.group(1)
            if "ebpf" in name or "bpf" in name:
                ebpf_pkg = name
                ebpf_path = path
                print(f"[+] Found eBPF Package: {name} at {path}")
            elif name != "wave-path-ebpf-lyapunov":
                daemon_pkg = name
                daemon_path = path
                print(f"[+] Found Daemon Package: {name} at {path}")

# إذا وجدنا مجلد النواة، ننشئ له ملف config خاص به في محيطه فقط
if ebpf_pkg:
    ebpf_dir = os.path.dirname(os.path.abspath(ebpf_path))
    cargo_dir = os.path.join(ebpf_dir, ".cargo")
    os.makedirs(cargo_dir, exist_ok=True)
    with open(os.path.join(cargo_dir, "config.toml"), "w", encoding="utf-8") as f:
        f.write("[build]\ntarget = \"bpfel-unknown-none\"\n\n[unstable]\nbuild-std = [\"core\"]\n")
    print(f"[+] Configured isolated target for eBPF package: {ebpf_pkg}")
'

# حفظ أسماء الحزم أو بنائها مباشرة
echo "[*] Step 4: Building eBPF kernel using Nightly toolchain..."
EBPF_DIR=""
for d in */; do
    if [ -f "${d}Cargo.toml" ] && [ -d "${d}.cargo" ]; then
        EBPF_DIR="${d%/}"
        break
    fi
done

if [ -n "$EBPF_DIR" ]; then
    "$HOME/.local-rust/bin/cargo" build --manifest-path "${EBPF_DIR}/Cargo.toml" --target bpfel-unknown-none -Z build-std=core --target-dir target-ebpf --release
fi

echo "[*] Step 5: Building user-space daemon using System Cargo (Pure std environment)..."
# بناء الفضاء المستخدم بمستودع ترمكس المستقر حصرياً ودون أي تداخل
/data/data/com.termux/files/usr/bin/cargo build --release

echo "[SUCCESS] Build pipeline finished successfully!"

# الإقلاع الفوري
if [ -f "./target/release/wave-path-daemon" ]; then
    ./target/release/wave-path-daemon
elif [ -f "./target/release/wave_path_daemon" ]; then
    ./target/release/wave_path_daemon
else
    /data/data/com.termux/files/usr/bin/cargo run --release
fi
