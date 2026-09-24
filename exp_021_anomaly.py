import time

# محاكاة BPF Ring Buffer لتخزين تنبيهات الشذوذ الاستباقي
bpf_ring_buffer = []

def validate_lyapunov_stability(current_v, previous_v):
    v_dot = current_v - previous_v
    if v_dot > 0:
        return False  # انتهاك شرط الاستقرار (شذوذ)
    return True       # استقرار التشغيل

def process_traffic_stream(node_id, traffic_packets):
    print(f"=== EXP-021: Proactive Anomaly Injection for Node {node_id:#04x} ===")
    prev_v = 500  # القيمة الابتدائية لاستقرار ليابونوف
    
    for i, packet in enumerate(traffic_packets):
        start_time = time.perf_counter_ns()
        
        # حساب القيمة الجديدة لدالة ليابونوف بناءً على التدفق المحقون
        current_v = prev_v + packet['delta_v']
        is_stable = validate_lyapunov_stability(current_v, prev_v)
        
        end_time = time.perf_counter_ns()
        latency = (end_time - start_time) / 1_000_000.0
        
        print(f"Packet #{i+1} | V(x): {current_v} | V_dot: {current_v - prev_v:+d} | Latency: {latency:.3f} ms")
        
        if not is_stable:
            alert = {
                "node_id": node_id,
                "packet_index": i+1,
                "v_x": current_v,
                "timestamp": time.time()
            }
            bpf_ring_buffer.append(alert)
            print(f"--> [ALERT] Proactive Anomaly Detected! Ring Buffer Queued. Action: XDP_DROP.")
        else:
            print(f"--> [PASS] Normal Stable Traffic. Action: XDP_PASS.")
            
        prev_v = current_v

if __name__ == "__main__":
    # تدفق حزم يحتوي على بيانات طبيعية تليها حالات حقن شذوذ مصطنعة
    test_packets = [
        {"delta_v": -15},  # تدفق طبيعي (استقرار متزايد)
        {"delta_v": -5},   # تدفق طبيعي مستقر
        {"delta_v": 95},   # [حقن شذوذ أول]: ارتفاع حاد يخرق مشتقة ليابونوف
        {"delta_v": -30},  # محاولة استقرار تالية
        {"delta_v": 120}   # [حقن شذوذ ثانٍ]: اختراق هيكلي خطير
    ]
    
    process_traffic_stream(0x05, test_packets)
    print(f"\n=== EXP-021 Summary ===")
    print(f"Total Proactive Alerts Captured in Ring Buffer: {len(bpf_ring_buffer)}")
    print("=== Test Completed Successfully ===")
