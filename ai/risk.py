from enum import Enum
class Risk(str, Enum):
    LOW='low'; MEDIUM='medium'; HIGH='high'

def classify(dVdt: float, anomaly_score: float, high_dvdt: float=0.0, high_anomaly: float=0.85) -> Risk:
    if dVdt > high_dvdt or anomaly_score >= high_anomaly:
        return Risk.HIGH
    if anomaly_score >= 0.50:
        return Risk.MEDIUM
    return Risk.LOW
