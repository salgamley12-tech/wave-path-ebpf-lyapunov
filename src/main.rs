mod lyapunov_verifier;
use lyapunov_verifier::SovereignState;

fn main() {
    println!("==> AQI Sovereign Kernel: Wave Path 3.0 Active");

    // اختبار حالات مختلفة للنظام مقابل عتبة الاستقرار الرياضي
    let safe_state = SovereignState::new(0.5, 1.0);
    let critical_state = SovereignState::new(1.5, 1.0);

    println!("[*] Evaluating state X = 0.5 (Threshold: 1.0)...");
    if safe_state.verify_invariant() {
        println!("✅ [PASS] النظام مستقر تماماً وفقاً لمعايير الحتمية الرياضية (Lyapunov V(x) <= Threshold).");
    } else {
        println!("⚠️ [FAIL] تحذير: تجاوز حدود استقرار النظام!");
    }

    println!("[*] Evaluating state X = 1.5 (Threshold: 1.0)...");
    if critical_state.verify_invariant() {
        println!("✅ [PASS] النظام مستقر تماماً.");
    } else {
        println!("⚠️ [FAIL] تم رصد عدم استقرار! تم تفعيل الحماية الحتمية.");
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_lyapunov_stability() {
        let state = SovereignState::new(0.8, 1.0);
        assert!(state.verify_invariant());

        let unstable_state = SovereignState::new(1.2, 1.0);
        assert!(!unstable_state.verify_invariant());
    }
}
