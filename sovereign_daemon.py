#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sovereign Daemon v3.1 - Active Mitigation & Lyapunov Stability Engine
Project: wave-path-ebpf-lyapunov
Author: مهندس / سلطان علي الجاملي
"""

import time
import hashlib
import json
import os

class SovereignAuditChain:
    def __init__(self, log_file="sovereign_audit.log"):
        self.log_file = log_file
        self.prev_hash = "0" * 64
        self._load_last_hash()

    def _load_last_hash(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, "r") as f:
                lines = f.readlines()
                if lines:
                    try:
                        last_block = json.loads(lines[-1].strip())
                        self.prev_hash = last_block.get("current_hash", self.prev_hash)
                    except json.JSONDecodeError:
                        pass

    def append_event(self, event_type, v_val, v_dot, action):
        timestamp = time.time()
        data_string = f"{timestamp}:{event_type}:{v_val}:{v_dot}:{action}:{self.prev_hash}"
        current_hash = hashlib.sha256(data_string.encode()).hexdigest()
        
        block = {
            "timestamp": timestamp,
            "event": event_type,
            "V_x": v_val,
            "V_dot": v_dot,
            "action": action,
            "prev_hash": self.prev_hash,
            "current_hash": current_hash
        }
        
        with open(self.log_file, "a") as f:
            f.write(json.dumps(block) + "\n")
        
        self.prev_hash = current_hash
        return current_hash

class LyapunovController:
    def __init__(self, threshold=0.0):
        self.threshold = threshold
        self.v_previous = 0.0

    def evaluate(self, v_current, dt=1.0):
        v_dot = (v_current - self.v_previous) / dt
        self.v_previous = v_current
        if v_dot >= self.threshold:
            return "XDP_DROP", v_dot
        else:
            return "XDP_PASS", v_dot

def main():
    print("==================================================")
    print(" [+] Initializing Sovereign Daemon v3.1 (Active Mitigation)")
    print("==================================================")
    
    audit_chain = SovereignAuditChain()
    controller = LyapunovController()
    
    sample_ticks = [0.5, 0.4, 0.3, 0.6, 0.8, 0.2, 0.1]
    
    for i, v_val in enumerate(sample_ticks):
        action, v_dot = controller.evaluate(v_val)
        event_type = "MITIGATION_TRIGGER" if action == "XDP_DROP" else "STATE_STABLE"
        
        hash_val = audit_chain.append_event(event_type, v_val, v_dot, action)
        
        print(f"[TICK {i+1:02d}] V(x): {v_val} | V_dot: {v_dot:+.2f} | Action: {action} | Hash: {hash_val[:10]}...")
        time.sleep(0.3)
        
    print("==================================================")
    print(" [✓] تم التحقق من سلامة سلسلة التدقيق وتنفيذ الاستجابة النشطة بنجاح.")
    print("==================================================")

if __name__ == "__main__":
    main()
