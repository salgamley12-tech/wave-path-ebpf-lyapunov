import hashlib
from datetime import datetime, timezone
import time

class SovereignAuditChain:
    def __init__(self, log_file="lyapunov_sovereign_secure.log"):
        self.log_file = log_file
        self.prev_hash = "0" * 64 # البذرة الأولى للنواة

    def record_tick(self, tick_id, states, v_val, v_dot):
        timestamp = datetime.now(timezone.utc).isoformat()
        payload = f"{tick_id}|{timestamp}|{states}|{v_val}|{v_dot}|{self.prev_hash}"
        
        current_hash = hashlib.sha256(payload.encode('utf-8')).hexdigest()
        log_entry = f"[{timestamp}] [TICK {tick_id:04d}] States: {states} | V(x): {v_val} | V_dot: {v_dot} | HASH: {current_hash}\n"
        
        with open(self.log_file, "a") as f:
            f.write(log_entry)
            
        self.prev_hash = current_hash
        return current_hash

if __name__ == "__main__":
    audit = SovereignAuditChain()
    print("=== AQI Sovereign Audit Daemon Active ===")
    for i in range(1, 6):
        states = f"[load: 0.{i}, entropy: 0.0{i}]"
        v_val = round(0.5 * (i * 0.1), 4)
        v_dot = -0.02 * i
        h = audit.record_tick(i, states, v_val, v_dot)
        print(f"[TICK {i:02d}] V(x)={v_val} | V_dot={v_dot} | Hash: {h[:16]}...")
        time.sleep(0.3)
    print("=== Audit Cycle Completed Successfully ===")
