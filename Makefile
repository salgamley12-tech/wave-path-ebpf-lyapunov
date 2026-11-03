TARGET = aarch64-unknown-none

all:
	cargo build --target $(TARGET) --release

clean:
	cargo clean
