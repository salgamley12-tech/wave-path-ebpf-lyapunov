mod lyapunov_verifier;
mod ebpf_filter;
mod sovereign_audit;

use lyapunov_verifier::SovereignState;
use ebpf_filter::{SovereignEbpfFilter, NetworkPacket};
use sovereign_audit::SovereignAuditor;

fn main() {
    println!("==> AQI Sovereign Kernel: Full Tri-Core Integration Active");

    let auditor = SovereignAuditor::new("STRICT");

    // 1. فحص الاستقرار الرياضي
    let state = SovereignState::new(0.4, 1.0);
    if state.verify_invariant() {
        auditor.record("Lyapunov", "PASS", "النظام مستقر رياضياً ضمن الحدود الآمنة.");
    } else {
        auditor.record("Lyapunov", "FAIL", "تجاوز حدود استقرار النظام!");
    }

    // 2. فحص الشبكة عبر eBPF
    let filter = SovereignEbpfFilter::new(0.8);
    let packet = NetworkPacket { 
        source_ip: 0xC0A80101, 
        packet_size: 512, 
        risk_score: 0.3 
    };
    
    if filter.inspect_packet(&packet) {
        auditor.record("eBPF", "ALLOW", "تم السماح بمرور الحزمة البرمجية.");
    } else {
        auditor.record("eBPF", "DROP", "تم اعتراض الحزمة لارتفاع مؤشر المخاطر.");
    }
}
