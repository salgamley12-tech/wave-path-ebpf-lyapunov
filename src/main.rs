mod lyapunov_verifier;
mod ebpf_filter;

use lyapunov_verifier::SovereignState;
use ebpf_filter::{SovereignEbpfFilter, NetworkPacket};

fn main() {
    println!("==> AQI Sovereign Kernel: eBPF & Lyapunov Integration Active");

    let state = SovereignState::new(0.4, 1.0);
    if state.verify_invariant() {
        println!("✅ [Lyapunov] النظام مستقر رياضياً.");
    }

    let filter = SovereignEbpfFilter::new(0.8);
    let incoming_packet = NetworkPacket {
        source_ip: 0xC0A80101,
        packet_size: 512,
        risk_score: 0.3,
    };

    if filter.inspect_packet(&incoming_packet) {
        println!("🛡️ [eBPF Filter] تم السماح بمرور الحزمة البرمجية بأمان تام.");
    } else {
        println!("🚨 [eBPF Filter] تم رصد خطر واعتراض الحزمة برمجياً!");
    }
}
