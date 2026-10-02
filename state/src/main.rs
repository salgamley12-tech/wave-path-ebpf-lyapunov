use wave_path_state::State;
fn main() {
    let observed=State{bytes_rate:1200.0,syscall_rate:12.0,connection_rate:4.0,anomaly_score:0.2};
    let baseline=State{bytes_rate:1000.0,syscall_rate:10.0,connection_rate:5.0,anomaly_score:0.0};
    println!("observed={observed:?}");
    println!("normalized={:?}",observed.normalize(baseline));
}
