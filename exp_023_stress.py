import time
import random

def validate_lyapunov_stability(current_v, previous_v):
    return (current_v - previous_v) <= 0

def run_stress_test(node_id, packet_count=1000):
    print(f"=== EXP-023: High-Load Stress Test for Node {node_id:#04x} ({packet_count} Packets) ===")
    
    prev_v = 500
    passed_count = 0
    dropped_count = 0
    start_total_time = time.perf_counter_ns()
    
    for _ in range(packet_count):
        # محاكاة تغير في دالة ليابونوف تحت ضغط الموارد
        delta_v = random.choice([-10, -5, -2, 0, 15, 50])  # قيم موجبة وسالبة عشوائية
        current_v = prev_v + delta_v
        
        if validate_lyapunov_stability(current_v, prev_v):
            passed_count += 1
            prev_v = current_v
        else:
            dropped_count += 1
            
    end_total_time = time.perf_counter_ns()
    total_time_ms = (end_total_time - start_total_time) / 1_000_000.0
    avg_latency_ns = (end_total_time - start_total_time) / packet_count

    print(f"Total Processed: {packet_count} Packets")
    print(f"Passed (Stable): {passed_count} | Dropped (Violations): {dropped_count}")
    print(f"Total Execution Time: {total_time_ms:.3f} ms")
    print(f"Average Processing Latency per Packet: {avg_latency_ns:.1f} ns")
    print("=== Test Completed Successfully ===")

if __name__ == "__main__":
    run_stress_test(node_id=0x0A, packet_count=1000)
