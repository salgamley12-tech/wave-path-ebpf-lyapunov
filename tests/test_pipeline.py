import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from controller.controller import Controller
from policy.policy import Action

class PipelineTest(unittest.TestCase):
    def test_high_risk_is_blocked(self):
        c=Controller()
        risk, action=c.process(0.0,(1,2),3.0,1.0,0.0,True)
        self.assertEqual(action,Action.DROP)
        self.assertEqual(c.path.points[-1].action,'drop')

    def test_unauthorized_is_observe_only(self):
        c=Controller()
        _, action=c.process(0.0,(1,2),3.0,1.0,0.9,False)
        self.assertEqual(action,Action.OBSERVE_ONLY)

if __name__=='__main__': unittest.main()
