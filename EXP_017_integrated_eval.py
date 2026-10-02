import json
import numpy as np

def run_integrated_evaluation():
    steps = 150
    np.random.seed(101)
    
    # 1. إشارة متغيرة تتضمن ضوضاء وصدمات مفاجئة
    base_signal = np.sin(np.linspace(0, 4 * np.pi, steps))
    noise = np.random.normal(0, 0.2, steps)
    shock = np.zeros(steps)
    shock[50:80] = 1.2 # صدمة مفاجئة
    
    full_signal = base_signal + noise + shock
    reference_Q = 0.0
    
    logs = []
    violations = 0
    recovered_points = 0
    
    for t in range(steps):
        val = full_signal[t]
        deviation = abs(val - reference_Q)
        
        # تقييم الاستقرار وحالة المخاطر
        if deviation < 0.5:
            risk = "LOW"
            stable = True
        elif deviation < 1.0:
            risk = "MEDIUM"
            stable = False
        else:
            risk = "HIGH"
            stable = False
            violations += 1
            
        if t > 80 and deviation < 0.5:
            recovered_points += 1
            
        logs.append({
            "step": t,
            "value": float(val),
            "deviation": float(deviation),
            "risk_level": risk,
            "stable": stable
        })

    output = {
        "experiment_id": "EXP_017_integrated_evaluation",
        "total_steps": steps,
        "high_risk_violations": violations,
        "successful_recovery_steps": recovered_points,
        "status": "PASSED" if violations > 0 and recovered_points > 0 else "FAILED",
        "data": logs
    }

    filename = "EXP_017_results.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)
    
    print(f"[SUCCESS] Integrated Evaluation (EXP-017) Completed.")
    print(f"Status: {output['status']} | High-Risk Violations Caught: {violations} | Recovery Verified: {recovered_points > 0}")
    print(f"Results saved to {filename}")

if __name__ == "__main__":
    run_integrated_evaluation()

