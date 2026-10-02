#include <linux/bpf.h>
#include <bpf/bpf_helpers.h>
#include <linux/if_ether.h>
#include <linux/ip.h>

struct {
    __uint(type, BPF_MAP_TYPE_HASH);
    __uint(max_entries, 10240);
    __type(key, __be32);
    __type(value, __u8);
} blocked_ips SEC(".maps");

SEC("xdp")
int wave_path_xdp_filter(struct xdp_md *ctx) {
    void *data_end = (void *)(long)ctx->data_end;
    void *data     = (void *)(long)ctx->data;
    struct ethhdr *eth = data;
    if ((void *)(eth + 1) > data_end || eth->h_proto != __constant_htons(ETH_P_IP)) return XDP_PASS;
    struct iphdr *iph = data + sizeof(*eth);
    if ((void *)(iph + 1) > data_end) return XDP_PASS;
    __be32 src_ip = iph->saddr;
    __u8 *blocked = bpf_map_lookup_elem(&blocked_ips, &src_ip);
    if (blocked && *blocked == 1) return XDP_DROP;
    return XDP_PASS;
}
char _license[] SEC("license") = "GPL";
