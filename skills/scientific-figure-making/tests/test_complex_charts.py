import sys,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'examples'))
from nature_complex_gallery import cluster_rows,correlation_order,flow_tables
from scipy.cluster.hierarchy import leaves_list

class CompositeContracts(unittest.TestCase):
    def test_z_score_and_orders(self):
        a=np.array([[1,2,5,6],[9,8,4,1],[1,4,3,6]],float);old=a.copy();z,t=cluster_rows(a)
        np.testing.assert_allclose(z.mean(axis=1),0,atol=1e-14);np.testing.assert_allclose(z.std(axis=1,ddof=1),1)
        self.assertEqual(sorted(leaves_list(t)),[0,1,2]);np.testing.assert_equal(a,old)
    def test_constant_feature_rejected(self):
        with self.assertRaises(ValueError):cluster_rows([[1,1],[2,3]])
    def test_correlation_exact_pair(self):
        r,t=correlation_order([[1,2,6],[2,4,3],[3,6,2],[4,8,1]])
        self.assertAlmostEqual(r[0,1],1);np.testing.assert_allclose(r,r.T);np.testing.assert_allclose(np.diag(r),1)
    def test_flow_identity_conservation(self):
        a=np.array([[0,1,0],[0,1,1],[1,0,1],[1,1,1]])
        x,y=flow_tables(a,[2,2,2]);np.testing.assert_equal(x,[[0,2],[1,1]])
        np.testing.assert_equal(x.sum(axis=0),y.sum(axis=1));self.assertEqual(x.sum(),4);self.assertEqual(y.sum(),4)
    def test_invalid_flow_categories(self):
        for a in [[[0,-1]],[[0,2]],[[0.,1.]]]:
            with self.assertRaises(ValueError):flow_tables(a,[2,2])
if __name__=='__main__':unittest.main()
