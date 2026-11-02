import sys,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from narrative_data import variant,corrupt
class NarrativeContracts(unittest.TestCase):
    def test_identity_operations(self):
        a=np.arange(64).reshape(8,8)%17
        for kind,amount in [('occlusion',0),('contrast',1),('shift',0)]:np.testing.assert_equal(variant(a,kind,amount),a)
    def test_zero_fill_no_wrap(self):
        a=np.ones((8,8))*16;b=variant(a,'shift',2);np.testing.assert_equal(b[:,:2],0);np.testing.assert_equal(b[:,2:],16)
    def test_mask_locality(self):
        a=np.ones((8,8))*16;b=variant(a,'occlusion',1);np.testing.assert_equal(b[2:6,2:6],0);self.assertEqual(b.sum(),48*16);np.testing.assert_equal(a,16)
    def test_shared_noise_and_clipping(self):
        a=np.ones((2,8,8))*8;n=np.ones_like(a);np.testing.assert_equal(corrupt(a,n,2,0),10);np.testing.assert_equal(corrupt(a,n,20,0),16);np.testing.assert_equal(a,8)
    def test_noise_zero_matches_mask(self):
        a=np.ones((2,8,8))*16;v=corrupt(a,np.zeros_like(a),0,.4)
        np.testing.assert_allclose(v[0],variant(a[0],'occlusion',.4))
    def test_invalid_levels(self):
        with self.assertRaises(ValueError):variant(np.zeros((8,8)),'shift',1.5)
        with self.assertRaises(ValueError):variant(np.zeros((8,8)),'occlusion',2)
        with self.assertRaises(ValueError):corrupt(np.zeros((2,8,8)),np.zeros((1,8,8)),0,0)
if __name__=='__main__':unittest.main()
