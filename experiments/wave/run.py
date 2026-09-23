import os, sys
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
sys.path.insert(0,ROOT)
from model.wave.damped_wave import Config, run
from controller.controller import Controller

out=os.path.join(ROOT,'experiments','wave','wave_output.csv')
rows=run(Config(seconds=2.0), out)
c=Controller()
for t,u,v,V,dV in rows:
    c.process(t, (u,v), V, dV, anomaly_score=min(abs(dV)/20.0,1.0), authorized=True)
print(f'samples={len(rows)}')
print(f'initial_V={rows[0][3]:.9f}')
print(f'final_V={rows[-1][3]:.9f}')
print(f'path_points={len(c.path.points)}')
print(f'output={out}')
