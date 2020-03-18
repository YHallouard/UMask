import unittest
from UMask.GEOMask import _get_raster_coords, Mask2GEOPoly
from UMask.UMask import *
import numpy as np
from shapely.wkt import loads


class TestStringMethods(unittest.TestCase):

    def test_get_raster_should_return_a_4_by_2_shape_matrix(self):
        # GIVEN
        path = './test/1709285_RGB.tif'

        expected_res = (4, 2)

        # WHEN
        res = _get_raster_coords(path=path)['coords'].shape

        # THEN
        self.assertEqual(expected_res, res)

    def test_get_raster_should_return_a_2_shape_list(self):
        # GIVEN
        path = './test/1709285_RGB.tif'

        im = Image.open(path)
        expected_res = np.asarray(im.size).shape

        # WHEN
        res = np.asarray(_get_raster_coords(path=path)['img_shape']).shape

        # THEN
        self.assertEqual(expected_res, res)

    def test_get_raster_should_return_shape_result(self):
        # GIVEN
        path = './test/1709285_RGB.tif'

        im = Image.open(path)
        expected_shape = im.size

        expected_res = 0

        # WHEN
        res = np.sum(np.asarray(_get_raster_coords(path=path)['img_shape']) - expected_shape)

        # THEN
        self.assertEqual(expected_res, res)

    def test_get_raster_should_return_result(self):
        # GIVEN
        path = './test/1709285_RGB.tif'

        ground_truth = np.array([[450640.3, 5404451.2],
                                 [450640.3, 5404351.1],
                                 [450740.2, 5404351.1],
                                 [450740.2, 5404451.2]])

        # WHEN
        res = np.sum(np.sum((_get_raster_coords(path=path)['coords'] - ground_truth) ** 2, 1)) < 1E-10

        # THEN
        self.assertTrue(res)

    def test_Mask2GEOPoly_should_return_a_string(self):
        # GIVEN
        pict_raster = np.array([[450640.3, 5404451.2],
                                [450640.3, 5404351.1],
                                [450740.2, 5404351.1],
                                [450740.2, 5404451.2]])

        coords = loads('MULTIPOLYGON (((600 600, 600 400, 400 400, 400 600, 600 600)))')

        img_shape = [1000, 1000]

        # WHEN
        res = Mask2GEOPoly(raster=pict_raster, poly_wkt=coords, img_shape=img_shape)

        # THEN
        self.assertTrue(isinstance(res, str))

    def test_Mask2GEOPoly_should_return_poly_translated_in_the_picture_raster(self):
        # GIVEN
        pict_raster = np.array([[450640.3, 5404451.2],
                                [450640.3, 5404351.1],
                                [450740.2, 5404351.1],
                                [450740.2, 5404451.2]])

        coords = loads('MULTIPOLYGON (((600 600, 600 400, 400 400, 400 600, 600 600)))')

        img_shape = [1000, 1000]

        window = Polygon(pict_raster)

        # WHEN
        res = window.contains(loads(Mask2GEOPoly(raster=pict_raster, poly_wkt=coords, img_shape=img_shape)))

        # THEN
        self.assertTrue(res)

    def test_Mask2GEOPoly_should_return_the_raster(self):
        # GIVEN
        pict_raster = np.array([[450640.3, 5404451.2],
                                [450640.3, 5404351.1],
                                [450740.2, 5404351.1],
                                [450740.2, 5404451.2]])
        coords = loads('MULTIPOLYGON (((1000 1000, 1000 0, 0 0, 0 1000, 1000 1000)))')

        img_shape = [1000, 1000]

        x_min = np.min(pict_raster[:, 0])
        x_max = np.max(pict_raster[:, 0])
        y_min = np.min(pict_raster[:, 1])
        y_max = np.max(pict_raster[:, 1])

        # WHEN
        res_poly = loads(Mask2GEOPoly(raster=pict_raster, poly_wkt=coords, img_shape=img_shape)).envelope.boundary.coords[
                   :]

        x = min([res_poly[0][0], res_poly[1][0], res_poly[2][0], res_poly[3][0]])
        X = max([res_poly[0][0], res_poly[1][0], res_poly[2][0], res_poly[3][0]])
        y = min([res_poly[0][1], res_poly[1][1], res_poly[2][1], res_poly[3][1]])
        Y = max([res_poly[0][1], res_poly[1][1], res_poly[2][1], res_poly[3][1]])

        res = (np.abs(x_min - x) + np.abs(x_max - X) + np.abs(y_min - y) + np.abs(y_max - Y))<0.01

        # THEN
        self.assertTrue(res)
