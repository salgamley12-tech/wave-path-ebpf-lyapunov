pub struct SovereignState {
    pub metric_x: f64,
    pub stability_threshold: f64,
}

impl SovereignState {
    pub fn new(metric_x: f64, stability_threshold: f64) -> Self {
        Self { metric_x, stability_threshold }
    }

    pub fn verify_invariant(&self) -> bool {
        let v_x = self.metric_x * self.metric_x;
        v_x <= self.stability_threshold
    }
}
