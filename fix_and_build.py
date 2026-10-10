import os
import glob
import subprocess

print("[*] Starting automated environment isolation and build pipeline...")

# 1. Ensure nightly toolchain path is active
os.environ["PATH"] = f"{os.path.expanduser('~/.local-rust/bin')}:" + os.environ.get("PATH", "")

# 2. Locate eBPF kernel crate directory
ebpf_dir = None
for path in glob.glob("**/Cargo.toml", recursive=True):
    if path == "Cargo.toml":
        continue
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if "bpf" in content or "ebpf" in path.lower() or "kernel" in path.lower():
        ebpf_dir = os.path.dirname(path)
        break

print(f"[+] Detected eBPF kernel directory: {ebpf_dir}")

# 3. Clean root Cargo.toml workspace members to decouple standard and no_std builds
if os.path.exists("Cargo.toml"):
    with open("Cargo.toml", "r", encoding="utf-8") as f:
        root_toml = f.read()
    
    if "[workspace]" in root_toml and ebpf_dir:
        lines = root_toml.splitlines()
        new_lines = []
        in_members = False
        for line in lines:
            if "members" in line and "[" in line:
                in_members = True
            if in_members:
                if ebpf_dir in line:
                    print(f"[-] Removing {ebpf_dir} from root workspace members to prevent flag leakage.")
                    continue
                if "]" in line:
                    in_members = False
            new_lines.append(line)
        root_toml = "\n".join(new_lines)
        with open("Cargo.toml", "w", encoding="utf-8") as f:
            f.write(root_toml)

# 4. Clean previous build artifacts for a fresh start
print("[+] Cleaning previous build states...")
subprocess.run(["cargo", "clean"], check=False)
if os.path.exists("Cargo.lock"):
    os.remove("Cargo.lock")

# 5. Build eBPF kernel independently with strict no_std isolation
if ebpf_dir:
    print(f"[+] Building eBPF kernel crate at {ebpf_dir}...")
    os.makedirs(os.path.join(ebpf_dir, ".cargo"), exist_ok=True)
    ebpf_config = '''[build]
target = "bpfel-unknown-none"

[unstable]
build-std = ["core"]
'''
    with open(os.path.join(ebpf_dir, ".cargo", "config.toml"), "w", encoding="utf-8") as cf:
        cf.write(ebpf_config)

    subprocess.run([
        "cargo", "build",
        "--manifest-path", os.path.join(ebpf_dir, "Cargo.toml"),
        "--target", "bpfel-unknown-none",
        "-Z", "build-std=core",
        "--release"
    ], check=True)

# 6. Build User-space Daemon normally using std
print("[+] Building user-space daemon (wave-path-daemon)...")
subprocess.run(["cargo", "build", "--release", "--bin", "wave-path-daemon"], check=True)

print("[SUCCESS] Build pipeline completed successfully! Launching daemon...")
