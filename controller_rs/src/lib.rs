use wave_path_state::State;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Risk { Low, Medium, High }
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Action { ObserveOnly, Pass, Drop }

pub fn classify(dvdt:f64, anomaly:f64)->Risk {
    if dvdt > 0.0 || anomaly >= 0.85 { Risk::High }
    else if anomaly >= 0.50 { Risk::Medium }
    else { Risk::Low }
}

pub fn guard(risk:Risk, authorized:bool)->Action {
    if !authorized { Action::ObserveOnly }
    else if matches!(risk,Risk::High) { Action::Drop }
    else { Action::Pass }
}

pub fn process(state:State, dvdt:f64, authorized:bool)->(Risk,Action) {
    let r=classify(dvdt,state.anomaly_score);
    (r,guard(r,authorized))
}
