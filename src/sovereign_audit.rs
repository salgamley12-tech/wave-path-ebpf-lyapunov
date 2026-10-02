pub struct SovereignAuditor {
    pub log_level: String,
}

impl SovereignAuditor {
    pub fn new(log_level: &str) -> Self {
        Self {
            log_level: log_level.to_string(),
        }
    }

    pub fn record(&self, module: &str, status: &str, message: &str) {
        println!("[AUDIT][{}] {} -> {}: {}", self.log_level, module, status, message);
    }
}
