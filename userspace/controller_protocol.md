# Userspace ↔ kernel contract

1. Telemetry collector receives events.
2. State engine aggregates them into a bounded feature vector.
3. Lyapunov/risk layer evaluates state trajectory.
4. Policy Guard validates the proposed action.
5. Only then may the userspace loader update the XDP blocklist map.
6. Every map update must log: timestamp, policy version, state hash, reason, action, and result.

The reference implementation deliberately does not provide an automatic mechanism for changing arbitrary firewall rules. Enforcement is limited to the explicit bounded blocklist contract.
