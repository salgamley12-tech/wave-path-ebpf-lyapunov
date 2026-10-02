"""Synthetic defensive telemetry stream; no real traffic is generated."""
import math
from telemetry.events import Event

def generate(n=200):
    for i in range(n):
        t=i*0.01
        burst=1.0 if 1.0 <= t <= 1.5 else 0.0
        yield Event(t,'synthetic','connection',int(100*(1+5*burst)),pid=100+i%3,authorized=not bool(burst))
