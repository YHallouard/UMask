from PIL import Image
from PIL import ImageDraw
import numpy as np
import os
import rasterio
from UMask.UMask import Poly2Mask, Mask2Poly
from shapely.geometry import Polygon, MultiPolygon, LinearRing
from shapely.wkt import loads
import shapely


def _get_raster_coords(path=''):
    # Coords computing
    ds = rasterio.open(path)

    coords = np.zeros((4, 2))
    coords[0, :] = [ds.bounds.left, ds.bounds.top]
    coords[1, :] = [ds.bounds.left, ds.bounds.bottom]
    coords[2, :] = [ds.bounds.right, ds.bounds.bottom]
    coords[3, :] = [ds.bounds.right, ds.bounds.top]

    # img_shape computing
    im = Image.open(path)
    width, height = im.size

    return {'coords':coords, 'img_shape':[width, height]}


def Mask2GEOPoly(raster=None, poly_wkt=None, img_shape=[None, None]):
    windows = [[0, img_shape[1]], [0, 0], [img_shape[0], 0], [img_shape[0], img_shape[1]]]
    poly_bbox_raster = Polygon(windows)

    picture_bbox_raster = Polygon(raster)

    shapes_poly = poly_wkt

    # We transform the coordinate in a GIS object of the shapely package
    (x_old, y_old) = poly_bbox_raster.centroid.coords[:][0]

    (x_shapes, y_shapes) = shapes_poly.centroid.coords[:][0]

    (x_raster, y_raster) = picture_bbox_raster.centroid.coords[:][0]

    scale_x = np.abs(np.max(raster[:, 0]) - np.min(raster[:, 0])) / np.mean(img_shape[0])
    scale_y = np.abs(np.max(raster[:, 1]) - np.min(raster[:, 1])) / np.mean(img_shape[1])

    # Scale
    #poly_bbox_raster = shapely.affinity.scale(poly_bbox_raster, scale_x, scale_y, origin=(x_old, y_old))
    shapes_poly = shapely.affinity.scale(shapes_poly, scale_x, -scale_y, origin=(x_shapes, y_shapes))

    # Translation
    #poly_bbox_raster = shapely.affinity.translate(poly_bbox_raster, -x_old + x_raster, -y_old + y_raster)
    shapes_poly = shapely.affinity.translate(shapes_poly, -x_old + x_raster, -y_old + y_raster)

    return shapes_poly.wkt
