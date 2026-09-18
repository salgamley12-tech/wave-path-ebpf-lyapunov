#!/usr/bin/env python3
import os, sys, json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,ROOT)
from model.wave.damped_wave import Config, run
from controller.controller import Controller

out=os.path.join(ROOT,'experiments','wave','wave_output.csv')
rows=run(Config(seconds=2.0),out)
c=Controller()
for t,u,v,V,dV in rows:
    # Demo anomaly signal is synthetic and intentionally simple.
    anomaly=min(abs(dV)/20.0,1.0)
    c.process(t,(u,v),V,dV,anomaly,authorized=True)
summary={
    'samples':len(rows),
    'initial_V':rows[0][3],
    'final_V':rows[-1][3],
    'energy_decreased':rows[-1][3] < rows[0][3],
    'path_points':len(c.path.points),
    'actions':{
        'pass':sum(p.action=='pass' for p in c.path.points),
        'drop':sum(p.action=='drop' for p in c.path.points),
        'observe_only':sum(p.action=='observe_only' for p in c.path.points),
    }
}
with open(os.path.join(ROOT,'experiments','wave','demo_summary.json'),'w') as f:
    json.dump(summary,f,indent=2)
print(json.dumps(summary,indent=2))
