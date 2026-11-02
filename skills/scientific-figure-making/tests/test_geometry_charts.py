import sys,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from geometry_charts import ternary_xy,field,crop_mask
class GeometryContracts(unittest.TestCase):
    def test_vertices_and_centroid(self):
        np.testing.assert_allclose(ternary_xy(np.eye(3)),[[0,0],[1,0],[.5,np.sqrt(3)/2]])
        np.testing.assert_allclose(ternary_xy([[1/3]*3]),[[.5,np.sqrt(3)/6]])
    def test_no_silent_normalization(self):
        for a in [[[1,1,1]],[[-.1,.5,.6]],[[1,float('nan'),0]]]:
            with self.assertRaises(ValueError):ternary_xy(a)
    def test_divergence_free(self):
        x,y=np.meshgrid(np.linspace(.1,1.9,9),np.linspace(.1,.9,7));h=1e-5
        du=(field(x+h,y)[0]-field(x-h,y)[0])/(2*h);dv=(field(x,y+h)[1]-field(x,y-h)[1])/(2*h)
        np.testing.assert_allclose(du+dv,0,atol=1e-9)
    def test_wall_normal_velocity(self):
        for y in [0,1]:np.testing.assert_allclose(field(np.linspace(0,2,9),y)[1],0,atol=1e-15)
    def test_nested_identity(self):
        xy=np.array([[0,0],[1,1],[2,2],[3,3]])
        outer=crop_mask(xy,[0,2,0,2]);inner=crop_mask(xy,[1,2,1,2]);self.assertTrue(np.all(~inner|outer));np.testing.assert_equal(np.where(inner)[0],[1,2])
    def test_crop_bounds(self):
        with self.assertRaises(ValueError):crop_mask([[0,0]],[2,1,0,1])
if __name__=='__main__':unittest.main()
