from collections import deque

class WindowAggregator:
    def __init__(self, window=1.0):
        self.window=window; self.events=deque()
    def add(self,event):
        self.events.append(event)
        cutoff=event.timestamp-self.window
        while self.events and self.events[0].timestamp < cutoff:
            self.events.popleft()
    def features(self):
        if not self.events: return {'bytes_rate':0.0,'syscall_rate':0.0,'connection_rate':0.0}
        t0=self.events[0].timestamp; t1=self.events[-1].timestamp
        dt=max(t1-t0, 1e-3)
        b=sum(e.bytes for e in self.events)/dt
        s=sum(e.event_type=='syscall' for e in self.events)/dt
        c=sum(e.event_type=='connection' for e in self.events)/dt
        return {'bytes_rate':b,'syscall_rate':s,'connection_rate':c}
