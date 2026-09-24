import time

# مصفوفة العقد المحظورة شبكياً (Isolation Access Control List)
isolated_nodes = set()

def handle_inter_node_event(sender_node, target_node, v_dot_value):
    start_time = time.perf_counter_ns()
    
    # فحص ما إذا كانت العقدة محظورة مسبقاً
    if sender_node in isolated_nodes:
        end_time = time.perf_counter_ns()
        latency = (end_time - start_time) / 1_000_000.0
        print(f"[Mesh Router] Node {sender_node:#04x} -> Node {target_node:#04x} | Latency: {latency:.3f} ms")
        print(f"--> [BLOCK] Node {sender_node:#04x} is ISOLATED. Action: XDP_DROP.")
        return "XDP_DROP"

    # التحقق من شرط الاستقرار لصد التهديدات
    if v_dot_value > 0:
        isolated_nodes.add(sender_node)
        end_time = time.perf_counter_ns()
        latency = (end_time - start_time) / 1_000_000.0
        print(f"[Mesh Router] Anomaly from Node {sender_node:#04x}! V_dot: +{v_dot_value} | Latency: {latency:.3f} ms")
        print(f"--> [ISOLATE] Instability Violation! Isolating Node {sender_node:#04x} across Mesh. Action: XDP_DROP.")
        return "XDP_DROP"

    end_time = time.perf_counter_ns()
    latency = (end_time - start_time) / 1_000_000.0
    print(f"[Mesh Router] Node {sender_node:#04x} -> Node {target_node:#04x} | Latency: {latency:.3f} ms")
    print(f"--> [PASS] Inter-Node Sync Stable. Action: XDP_PASS.")
    return "XDP_PASS"

if __name__ == "__main__":
    print("=== EXP-022: Distributed Node Isolation Simulation ===")
    
    print("\n--- Step 1: Normal Communication Between Node 0x01 and Node 0x02 ---")
    handle_inter_node_event(sender_node=0x01, target_node=0x02, v_dot_value=-10)
    
    print("\n--- Step 2: Anomaly Triggered by Node 0x01 ---")
    handle_inter_node_event(sender_node=0x01, target_node=0x02, v_dot_value=150)
    
    print("\n--- Step 3: Subsequent Communication Attempt from Isolated Node 0x01 ---")
    handle_inter_node_event(sender_node=0x01, target_node=0x03, v_dot_value=-5)
    
    print("\n=== EXP-022 Summary ===")
    print(f"Total Isolated Nodes in Mesh: {len(isolated_nodes)}")
    print("=== Test Completed Successfully ===")
