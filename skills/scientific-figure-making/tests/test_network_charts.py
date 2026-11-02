import sys,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'examples'))
from nature_network_gallery import edges
class EdgeContracts(unittest.TestCase):
    def test_signed_threshold_and_unique_pairs(self):
        self.assertEqual(edges([[1,.6,-.8],[.6,1,.1],[-.8,.1,1]]),[(1,0,.6),(2,0,-.8)])
    def test_invalid(self):
        with self.assertRaises(ValueError):edges([[1,.5],[.2,1]])
        with self.assertRaises(ValueError):edges([[1,0],[0,1]],1.1)
if __name__=='__main__':unittest.main()
