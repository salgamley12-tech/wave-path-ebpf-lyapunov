from dataclasses import dataclass
from typing import Iterable, List
import math, random

@dataclass(frozen=True)
class Observation:
    timestamp: float
    value: float
    noise: float

def observe(signal: Iterable[tuple], sigma: float = 0.0, seed: int = 7) -> List[Observation]:
    rng = random.Random(seed)
    out=[]
    for t, value in signal:
        eps = rng.gauss(0.0, sigma) if sigma else 0.0
        out.append(Observation(t, value + eps, eps))
    return out

def rmse(predicted, observed):
    p=list(predicted); o=list(observed)
    if len(p) != len(o) or not p:
        raise ValueError('equal non-empty sequences required')
    return math.sqrt(sum((a-b)**2 for a,b in zip(p,o))/len(p))
