from osgeo import gdal
import numpy as np
import math


def normalize(array):
    array_min, array_max = array.min(), array.max()
    return ((array - array_min) / (array_max - array_min) * 255).astype(np.uint8)


def stretch_histogram(band_array, min_percent=1, max_percent=99):

    min_val = np.percentile(band_array, min_percent)
    max_val = np.percentile(band_array, max_percent)
    
    stretched_band = np.clip((band_array - min_val) / (max_val - min_val), 0, 1)
    return (stretched_band * 255).astype(np.uint8)


def geo_to_pixel(transform, geo_x, geo_y):
    inv_transform = gdal.InvGeoTransform(transform)
    pixel_x = inv_transform[0] + geo_x * inv_transform[1] + geo_y * inv_transform[2]
    pixel_y = inv_transform[3] + geo_x * inv_transform[4] + geo_y * inv_transform[5]
    return int(pixel_x), int(pixel_y)

def degrees2mercator(lat, lon):
    # Rayon de la Terre en mètres pour Web Mercator
    R = 6378137.0

    # Conversion des degrés, minutes, secondes en radians
    lambda_rad = (lon[0] + lon[1]/60 + lon[2]/3600) * (math.pi / 180.0)
    phi_rad = (lat[0] + lat[1]/60 + lat[2]/3600) * (math.pi / 180.0)
    
    # Calcul de x en Web Mercator
    x = R * lambda_rad
    
    # Calcul de y en Web Mercator
    y = R * math.log(math.tan((math.pi / 4.0) + (phi_rad / 2.0)))
    
    return x, y
