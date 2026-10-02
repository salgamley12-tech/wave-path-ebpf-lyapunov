import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from telemetry.events import Event
from telemetry.aggregator import WindowAggregator

class TelemetryTest(unittest.TestCase):
    def test_window_aggregation(self):
        a=WindowAggregator(window=1.0)
        a.add(Event(0.0,'t','connection',100))
        a.add(Event(0.5,'t','syscall',50))
        f=a.features()
        self.assertGreater(f['bytes_rate'],0)
        self.assertGreater(f['syscall_rate'],0)

if __name__=='__main__': unittest.main()
