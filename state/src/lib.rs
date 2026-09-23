#[derive(Debug, Clone, Copy, Default, PartialEq)]
pub struct State { pub bytes_rate:f64, pub syscall_rate:f64, pub connection_rate:f64, pub anomaly_score:f64 }
impl State {
    pub fn normalize(self, b: State) -> State {
        fn n(x:f64,s:f64)->f64 { x / s.abs().max(1e-12) }
        State { bytes_rate:n(self.bytes_rate,b.bytes_rate), syscall_rate:n(self.syscall_rate,b.syscall_rate), connection_rate:n(self.connection_rate,b.connection_rate), anomaly_score:self.anomaly_score }
    }
}
