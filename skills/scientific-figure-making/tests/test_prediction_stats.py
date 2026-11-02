import sys,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from prediction_stats import validate,calibration_bins,net_benefit,treat_all
class PredictionContracts(unittest.TestCase):
    def test_endpoints_and_empty_bins(self):
        rows,e,b=calibration_bins([0,1],[0,1]);self.assertEqual(sum(v['n'] for v in rows),2);self.assertEqual([v['bin'] for v in rows],[0,9]);self.assertEqual(e,0);self.assertEqual(b,0)
    def test_known_brier_and_ece(self):
        rows,e,b=calibration_bins([0,1],[.25,.75],[0,.5,1]);self.assertAlmostEqual(e,.25);self.assertAlmostEqual(b,.0625)
        for v in rows:self.assertLessEqual(v['lo'],v['observed']);self.assertGreaterEqual(v['hi'],v['observed'])
    def test_decision_manual(self):
        y=[0,1,0,1];p=[.1,.8,.6,.4];np.testing.assert_allclose(net_benefit(y,p,[.5]),[0]);np.testing.assert_allclose(treat_all(y,[.5]),[0])
    def test_all_none_and_ties(self):
        y=[0,1,0,1];np.testing.assert_allclose(net_benefit(y,[1]*4,[.2,.6]),treat_all(y,[.2,.6]));np.testing.assert_equal(net_benefit(y,[0]*4,[.2,.6]),[0,0]);np.testing.assert_allclose(net_benefit([1,0],[.5,.1],[.5]),[.5])
    def test_invalid_data(self):
        for y,p in [([0,2],[.1,.2]),([0,1],[.1,float('nan')]),([0,1],[.1,1.1])]:
            with self.assertRaises(ValueError):validate(y,p)
        with self.assertRaises(ValueError):net_benefit([0,1],[.2,.4],[1])
    def test_invalid_bin_edges(self):
        with self.assertRaises(ValueError):calibration_bins([0,1],[.1,.9],[0,.5,.5,1])
if __name__=='__main__':unittest.main()
