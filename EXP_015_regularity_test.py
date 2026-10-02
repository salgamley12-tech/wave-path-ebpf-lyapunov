import json
import numpy as np

def evaluate_regularity():
    steps = 100
    np.random.seed(42)
    
    true_signal = np.sin(np.linspace(0, 2 * np.pi, steps))
    illusory_noise = np.random.normal(0, 0.5, steps)
    combined_signal = true_signal + illusory_noise

    results = []
    reference_Q = 0.0
    
    for t in range(steps):
        val = combined_signal[t]
        deviation = abs(val - reference_Q)
        is_true_regularity = True if deviation < 0.6 else False
        
        results.append({
            "step": t,
            "signal_value": val,
            "deviation": deviation,
            "true_regularity": is_true_regularity
        })

    output = {
        "experiment_id": "EXP_015_regularity_test",
        "description": "Distinguishing true regularity from illusory noise under dynamic conditions.",
        "data": results
    }

    filename = "EXP_015_results.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)
    
    print(f"[SUCCESS] Experiment EXP-015 executed successfully. Results saved to {filename}")

if __name__ == "__main__":
    evaluate_regularity()

