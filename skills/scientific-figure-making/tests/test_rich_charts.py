import sys,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import rich_charts as c

class StatisticalContracts(unittest.TestCase):
    def test_constant_paired_effect(self):
        mean,ci,boot=c.paired_effect([1,2,3],[4,5,6])
        self.assertEqual(mean,3);np.testing.assert_equal(ci,[3,3]);np.testing.assert_equal(boot,np.full(5000,3))
    def test_paired_lengths(self):
        with self.assertRaises(ValueError):c.paired_effect([1,2],[1,2,3])
    def test_ties(self):
        np.testing.assert_equal(c.ranks([[3,3,1],[1,2,3]]),[[1.5,1.5,3],[3,2,1]])
    def test_area_proportional(self):
        a=c.bubble_areas([0,50,100]);self.assertEqual(a[0],0);self.assertEqual(a[2]/a[1],2)
    def test_density_degenerate(self):
        x,p=c.density([2,2,2]);np.testing.assert_equal(x,[2]);np.testing.assert_equal(p,[0])
    def test_raw_data_preserved(self):
        a=np.array([1.,2.,3.,8.]);old=a.copy();c.density(a);c.paired_effect(a,a+1);np.testing.assert_equal(a,old)
    def test_nonfinite_rejected(self):
        with self.assertRaises(ValueError):c.density([1,np.nan])
if __name__=='__main__':unittest.main()
