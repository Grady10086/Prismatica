import sys,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from advanced_stats import km,at_risk,hill,fit_dose
class AdvancedContracts(unittest.TestCase):
    def test_tied_event_censor(self):
        t,s,lo,hi=km([1,1,2],[1,0,1]);np.testing.assert_allclose(s,[1,2/3,0]);np.testing.assert_equal(at_risk([1,1,2],[0,1,2,3]),[3,3,1,0])
        self.assertTrue(np.all(lo<=s));self.assertTrue(np.all(hi>=s))
    def test_all_censored(self):
        for v in km([1,2,3],[0,0,0])[1:]:np.testing.assert_equal(v,np.ones(4))
    def test_complete_failure(self):
        _,s,lo,hi=km([1,2,3],[1,1,1]);np.testing.assert_allclose(s,[1,2/3,1/3,0]);self.assertEqual(lo[-1],0);self.assertEqual(hi[-1],0)
    def test_input_validation(self):
        for t,e in [([0,1],[1,0]),([1,2],[1,2]),([1,float('nan')],[0,1])]:
            with self.assertRaises(ValueError):km(t,e)
    def test_hill_midpoint(self):
        self.assertAlmostEqual(float(hill(-.5,5,95,-.5,1.2)),50)
    def test_fit_recovers_parameters(self):
        x=np.linspace(-3,2,12);truth=[5,95,-.5,1.2];fit=fit_dose(x,hill(x,*truth));np.testing.assert_allclose(fit,truth,atol=1e-5)
    def test_five_distinct_doses(self):
        with self.assertRaises(ValueError):fit_dose([0,0,0,1,1],[1,2,3,4,5])
if __name__=='__main__':unittest.main()
