# XDP enforcement

The program implements a bounded IPv4 blocklist. The default is PASS. A userspace controller is expected to update `blocked_ips` only after Policy Guard authorization.

For a production build, use a Linux eBPF toolchain and pin the map so that the controller and XDP program can share policy state.
