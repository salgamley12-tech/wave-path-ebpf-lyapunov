import time

mesh_stability_map = {}

def validate_lyapunov_stability(current_v, previous_v):
    v_dot = current_v - previous_v
    if v_dot > 0:
        return False
    return True

def mock_node_packet_handler(node_id, current_v):
    start_time = time.perf_counter_ns()
    prev_v = mesh_stability_map.get(node_id, 500)
    is_stable = validate_lyapunov_stability(current_v, prev_v)
    mesh_stability_map[node_id] = current_v
    end_time = time.perf_counter_ns()
    sync_latency_ms = (end_time - start_time) / 1_000_000.0
    
    print(f"[Node Engine] Node ID: {node_id:#04x} | V(x): {current_v} | Latency: {sync_latency_ms:.3f} ms")
    
    if not is_stable:
        print("--> [ALERT] Lyapunov Violation Detected. Action: XDP_DROP.")
        return "XDP_DROP"
    else:
        print("--> [STATUS] System Stable. Action: XDP_PASS.")
        return "XDP_PASS"

if __name__ == "__main__":
    print("=== WPS-INP v3.0 & Lyapunov Simulation ===")
    print("\n--- Test 1: Stable State ---")
    mock_node_packet_handler(node_id=0x01, current_v=450)
    print("\n--- Test 2: Anomaly / Instability Detected ---")
    mock_node_packet_handler(node_id=0x01, current_v=600)
    print("\n=== Simulation Completed Successfully ===")
