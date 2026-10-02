pub struct NetworkPacket {
    pub source_ip: u32,
    pub packet_size: usize,
    pub risk_score: f64,
}

pub struct SovereignEbpfFilter {
    pub max_risk_threshold: f64,
}

impl SovereignEbpfFilter {
    pub fn new(max_risk_threshold: f64) -> Self {
        Self { max_risk_threshold }
    }

    pub fn inspect_packet(&self, packet: &NetworkPacket) -> bool {
        if packet.risk_score > self.max_risk_threshold {
            false 
        } else {
            true  
        }
    }
}
