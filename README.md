# UMask
This Package is a contribution to shapely, imantics and rasterio. It provides you with a function to convert Mask pictures into their WKT representation and another to create Mask from WKT object.

## Requirement

  - Python 3.6, 3.7, 3.8

## How to install ?

```
sudo pip install -e git+https://github.com/YHallouard/UMask.git#egg=UMask
```

## How to use UMask ?
```python
from UMask.UMask import Mask2Poly, Poly2Mask

Mask2Poly(Masks=MaskToTransform, empty_geom=True)
Poly2Mask(raw_mask=np.zeros((height, width)), polygons='POLYGON EMPTY',)
```
## How to use GEOUMask ?
```python
from UMask.UMask import Mask2Poly
from UMask.GEOMask import _get_raster_coords, Mask2GEOPoly
import matplotlib as plt

path_to_image = './images/test.tif'
path_to_mask  = './mask/test.png'

mask = plt.imread(path_to_mask)

# Getting Mask Wkt representation in pixel coordinate
poly = Mask2Poly(Masks=mask, empty_geom=True)

# Getting True image meta data
meta = _get_raster_coords(path=path_to_image)
raster = meta['coords']
img_shape = meta['img_shape']

# Getting Mask Wkt representation in GIS coordinate
geo_poly = Mask2GEOPoly(raster=raster, poly_wkt=poly, img_shape=img_shape)
```