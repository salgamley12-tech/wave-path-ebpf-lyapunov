import os, sys, tempfile, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from model.wave.damped_wave import Config, run

class WaveTest(unittest.TestCase):
    def test_energy_decreases(self):
        with tempfile.NamedTemporaryFile(delete=False) as f: p=f.name
        try:
            rows=run(Config(seconds=0.5),p)
            self.assertGreater(len(rows),100)
            self.assertLess(rows[-1][3],rows[0][3])
        finally:
            os.remove(p)

if __name__=='__main__': unittest.main()
