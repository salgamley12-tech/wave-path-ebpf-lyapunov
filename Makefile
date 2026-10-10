TARGET = xdp_lyapunov_kernel
CC = clang

all: $(TARGET).o

$(TARGET).o: $(TARGET).c
	$(CC) -target bpf -O2 -I. -c $< -o $@

clean:
	rm -f *.o
	rm -rf bpf
