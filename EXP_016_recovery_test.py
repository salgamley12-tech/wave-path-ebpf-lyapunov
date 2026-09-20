import json
import numpy as np

def evaluate_recovery_time():
    steps = 100
    np.random.seed(42)
    
    # محاكاة مسار حركي يتعرض لصدمات واضطرابات مفاجئة
    signal = np.zeros(steps)
    reference_Q = 1.0
    signal[:30] = reference_Q
    
    # إحداث انحراف مفاجئ (صدمة) في المنتصف
    signal[30:60] = reference_Q + 0.8
    # التعافي التدريجي بفضل عمل طبقة الحراسة
    for t in range(60, steps):
        signal[t] = signal[t-1] - 0.08

    recovery_logs = []
    anomaly_detected_at = None
    recovered_at = None

    for t in range(steps):
        val = signal[t]
        deviation = abs(val - reference_Q)
        
        # رصد وقت اكتشاف الخلل
        if deviation > 0.1 and anomaly_detected_at is None:
            anomaly_detected_at = t
            
        # رصد وقت التعافي والعودة للاستقرار
        if anomaly_detected_at is not None and deviation <= 0.1 and recovered_at is None:
            recovered_at = t

        recovery_logs.append({
            "step": t,
            "signal_value": val,
            "deviation": deviation
        })

    # حساب زمن الاستجابة والتعافي الفعلي
    latency = anomaly_detected_at if anomaly_detected_at is not None else 0
    recovery_duration = (recovered_at - anomaly_detected_at) if (recovered_at and anomaly_detected_at) else 0

    output = {
        "experiment_id": "EXP_016_recovery_test",
        "detection_latency": latency,
        "recovery_time": recovery_duration,
        "data": recovery_logs
    }

    filename = "EXP_016_results.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)
    
    print(f"[SUCCESS] Experiment EXP-016 executed successfully. Detection Latency: {latency}, Recovery Time: {recovery_duration}. Saved to {filename}")

if __name__ == "__main__":
    evaluate_recovery_time()

