from imantics import Mask
from shapely.geometry import Polygon, MultiPolygon, LinearRing
from shapely.wkt import loads
from tqdm import tqdm
import numpy as np
import pandas as pd
from PIL import ImageDraw, Image


class ValueError(Exception):
    pass


def Mask2Poly(Masks=None, empty_geom=True):
    """
    Creating a WKT representation of shape (polygons) on a Mask. On each Mask this function will return a poly or a
    multipolygon.
    Input : Masks = array of shape (nb masks, height, width)
            empty_geom = boolean : if you allow this function to create empty polygons if there is no polygons on it.
            If empty_geom is set to False, Mask2Poly will return a 2pixel height and width triangle as polygon
    Output : WKT representation of the Mask.

    :type Masks: object
    :type empty_geom: bool
    """
    if len(Masks.shape) < 3:
        raise ValueError('Masks shape is intended to be upper than 3. (nb of Mask, height, width)')

    # Create a list that will contains all polygons' wkt of all masks
    POLYGONS = []
    for i in tqdm(range(Masks.shape[0])):
        # Only 0 and 1 in the mask
        mask = (Masks[i] > 0.11).astype(np.int8)

        # Extract all polygons in Masks 
        polygons = Mask(mask).polygons()
        points = polygons.points

        poly = []
        Area = []
        for point in points:
            x = point[:, 0]
            y = point[:, 1]

            # Removing too polygons with less than two points (error)
            if len(x) > 2:
                coords = zip(x, y)
                p = Polygon(coords).buffer(0)
                if p.type.upper() == "MULTIPOLYGON":
                    poly.append(p[0])
                    Area.append(poly[-1].area)
                else:
                    poly.append(p)
                    Area.append(poly[-1].area)

        # empty geomn set to False allow to create a very small triangle to 
        # avoid an empty geometry
        if empty_geom == False:
            if len(poly) == 0:
                mini_mask = np.zeros((4, 4, 1))
                mini_mask[0, 0:2] = 1
                mini_mask[1, 0:1] = 1

                polygons = Mask(mini_mask).polygons()

                points = polygons.points

                poly = []
                Area = []
                for point in points:
                    x = point[:, 0]
                    y = point[:, 1]

                    if len(x) > 2:
                        coords = zip(x, y)
                        p = Polygon(coords).buffer(0)
                        if p.type.upper() == "MULTIPOLYGON":
                            poly.append(p[0])
                            Area.append(poly[-1].area)
                        else:
                            poly.append(p)
                            Area.append(poly[-1].area)

        new_poly = []
        if len(poly)>0:
            # Sort polygons by Area and assign polygons contained by an other as a hole
            r = pd.DataFrame(poly)
            r.columns = ['poly']
            r['Aera'] = Area

            r = r.sort_values(by=['Aera'], ascending=False)
            poly = list(r['poly'].values)


            i = 0
            while i < len(poly):
                temp = poly[i].buffer(0)
                j = i + 1
                while j < len(poly):
                    if poly[i].contains(poly[j]):
                        ext = temp
                        inte = temp.interiors[:]
                        a = [inner for inner in inte]
                        a.append(LinearRing(list(poly[j].exterior.coords[:])))
                        inte = a
                        temp = Polygon(ext.exterior.coords[:], inte)
                        poly.remove(poly[j])
                    else:
                        j += 1
                i += 1
                new_poly.append(temp)

        m = MultiPolygon(new_poly)
        POLYGONS.append(str(m.buffer(0).wkt))
    return POLYGONS


#print(Mask2Poly(Masks=np.zeros((3,255,255)), empty_geom=True))

def Poly2Mask(raw_mask=None, polygons=None):
    """
    Create a Mask from a WKT object
    Input : raw_mask = nul array of shape (height, width)
            polygons = wkt object
    Output : Mask with drawn polygons

    :type raw_mask: object
    :type polygons: bool
    """
    # Loading Mask
    mask = Image.fromarray((raw_mask.astype(np.uint8())))

    # Loading WKT representation
    poly = loads(polygons)

    # Draw object, we'll draw polygons on it
    im = mask
    draw = ImageDraw.Draw(im)

    if str(poly)=='POLYGON EMPTY':
        return im

    if poly.type.upper() == "MULTIPOLYGON":
        # nb_polygones = len(poly.geoms)
        for i_polygone in poly.geoms:
            tpolygon_contours = i_polygone.exterior.coords[:]

            # For shape of polygones
            e = np.array(tpolygon_contours).round().astype(int)
            x = e[:, 0]
            y = e[:, 1]

            # convert values to ints
            x = map(int, x)
            y = map(int, y)

            draw.polygon(list(zip(x, y)), fill=(255))

            # For Holes in Polygones
            for tpolygon_trous in i_polygone.interiors:
                i_tpolygon_trou = tpolygon_trous.coords[:]
                e = np.array(i_tpolygon_trou).round().astype(int)
                x = e[:, 0]
                y = e[:, 1]

                # convert values to ints
                x = map(int, x)
                y = map(int, y)

                draw.polygon(list(zip(x, y)), fill=(0))

    elif poly.type.upper() == "POLYGON":
        # For shape of polygones
        tpolygon_contours = poly.exterior.coords[:]

        e = np.array(tpolygon_contours).round().astype(int)
        x = e[:, 0]
        y = e[:, 1]

        # convert values to ints
        x = map(int, x)
        y = map(int, y)

        draw.polygon(list(zip(x, y)), fill=(255))

        # For Holes in Polygones
        tpolygon_trous = poly.interiors

        for tpolygon_trous in poly.interiors:
            i_tpolygon_trou = tpolygon_trous.coords[:]
            e = np.array(i_tpolygon_trou).round().astype(int)
            x = e[:, 0]
            y = e[:, 1]

            # convert values to ints
            x = map(int, x)
            y = map(int, y)

            draw.polygon(list(zip(x, y)), fill=(0))

    return im


#print(np.array(Poly2Mask(raw_mask=np.zeros((4,4)), polygons='POLYGON EMPTY',)))
