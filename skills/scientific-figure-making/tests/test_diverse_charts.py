import sys,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'examples'))
from nature_diverse_gallery import pca,intersections
class DiverseContracts(unittest.TestCase):
    def test_exclusive_partition_and_set_sizes(self):
        a=np.array([[1,0],[1,1],[0,1],[1,0]])
        items=intersections(a);self.assertEqual(sum(n for _,n in items),len(a));self.assertEqual(dict(items)[(1,0)],2)
        np.testing.assert_equal(sum(np.array(p)*n for p,n in items),a.sum(axis=0))
    def test_binary_required(self):
        with self.assertRaises(ValueError):intersections([[1,2]])
    def test_pca_center_and_variance(self):
        a=np.array([[1.,2.],[2.,4.],[3.,6.]]);old=a.copy();pc,v=pca(a)
        np.testing.assert_allclose(pc.mean(axis=0),0,atol=1e-14);self.assertAlmostEqual(v[0],1);np.testing.assert_equal(a,old)
    def test_pca_degenerate(self):
        with self.assertRaises(ValueError):pca([[1,1],[1,1]])
if __name__=='__main__':unittest.main()
