CC = clang
CFLAGS = -O3 -Wall

all: sovereign_sim

sovereign_sim: main.c
$(CC)$(CFLAGS) main.c -o sovereign_sim
@echo "[+] Build complete. Running Sovereign Simulation..."
./sovereign_sim

clean:
rm -f sovereign_sim
@echo "[+] Cleaned build artifacts."
