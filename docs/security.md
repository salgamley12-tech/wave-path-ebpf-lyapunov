# Security boundaries

- XDP defaults to PASS.
- The blocklist is bounded at 1024 entries.
- Policy Guard is required before enforcement.
- The reference demo uses synthetic data.
- No credential collection, persistence, stealth, exploitation, or destructive automation is included.
- Production deployments require privilege separation, audit logging, map pinning controls, rollback and fail-safe procedures.
