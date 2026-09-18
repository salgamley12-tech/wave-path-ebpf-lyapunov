from dataclasses import dataclass, asdict
import math

@dataclass(frozen=True)
class PathPoint:
    t: float
    state: tuple
    V: float
    dVdt: float
    risk: str
    action: str

def euclidean(a,b):
    return math.sqrt(sum((x-y)**2 for x,y in zip(a,b)))

class WavePath:
    def __init__(self):
        self.points=[]
    def append(self, point: PathPoint):
        if self.points and point.t < self.points[-1].t:
            raise ValueError('time must be monotonic')
        self.points.append(point)
    def displacement(self):
        if len(self.points)<2: return 0.0
        return euclidean(self.points[0].state, self.points[-1].state)
    def as_dicts(self):
        return [asdict(p) for p in self.points]
