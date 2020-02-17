# UMask
This Package is a contribution to shapely and imantics. It provides you with a function to convert Mask pictures into their WKT representation and another to create Mask from WKT object.

## Requirement

  - Python 3.6

## How to install ?

sudo pip install -e git+https://github.com/YHallouard/UMask.git#egg=UMask

## How to use it ?

from UMask.UMask import Mask2Poly, Poly2Mask

Mask2Poly(Masks=MaskToTransform, empty_geom=True)
Poly2Mask(raw_mask=np.zeros((height, width)), polygons='POLYGON EMPTY',)
