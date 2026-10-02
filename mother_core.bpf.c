#define SEC(name) __attribute__((section(name), used))

struct bpf_map_def {
    unsigned int type;
    unsigned int key_size;
    unsigned int value_size;
    unsigned int max_entries;
    unsigned int map_flags;
};

SEC("kprobe/sys_enter")
int bpf_prog(void *ctx) {
    return 0;
}

char _license[] SEC("license") = "GPL";
