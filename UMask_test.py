import unittest
from UMask.UMask import Mask2Poly, Poly2Mask
import numpy as np


class TestStringMethods(unittest.TestCase):

    def test_identity_should_return_the_same_null_mask(self):
        # GIVEN
        tester = np.zeros((1, 256, 256))

        expected_res = 0

        # WHEN
        g = Mask2Poly(Masks=tester, empty_geom=True)
        f = Poly2Mask(raw_mask=np.zeros((256, 256)), polygons=g[0])

        res = np.sum(np.abs(tester[0] - np.array(f)))

        # THEN
        self.assertEqual(expected_res, res)
