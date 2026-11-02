import sys,unittest
from pathlib import Path
import numpy as np
from scipy.stats import false_discovery_control
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from inference_stats import bh,ora,meta
class InferenceContracts(unittest.TestCase):
    def test_bh_reference_and_ties(self):
        p=np.array([0,.01,.03,.03,.8,1]);np.testing.assert_allclose(bh(p),false_discovery_control(p,method='bh'))
    def test_ora_exact(self):
        result=ora(range(10),[0,1,4],{'S':[0,1,2,3]})[0];self.assertEqual(result['hits'],2);self.assertAlmostEqual(result['p'],1/3)
    def test_background_validation(self):
        with self.assertRaises(ValueError):ora(range(10),[11],{'S':[1]})
        with self.assertRaises(ValueError):ora(range(10),[1],{'S':[11]})
    def test_common_identical(self):
        r=meta([.2]*4,[.2]*4);self.assertEqual(r['tau2'],0);self.assertAlmostEqual(r['mean'],.2);self.assertAlmostEqual(r['se'],.1)
    def test_reml_heterogeneity_and_permutation(self):
        y=np.array([-1,0,.5,1.2]);s=np.array([.1,.2,.2,.1]);a=meta(y,s);b=meta(y[::-1],s[::-1]);self.assertGreater(a['tau2'],0);self.assertAlmostEqual(a['mean'],b['mean']);self.assertAlmostEqual(sum(a['weights']),1)
    def test_input_validation(self):
        with self.assertRaises(ValueError):bh([-.1,.2])
        with self.assertRaises(ValueError):meta([1,2,3],[0,.1,.1])
if __name__=='__main__':unittest.main()
