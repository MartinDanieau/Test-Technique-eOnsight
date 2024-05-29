from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt
from tools import normalize, stretch_histogram, geo_to_pixel, degrees2mercator


# Coordonnées des différents ponts exprimées en degrées, minutes et secondes
coords = {
    'Genes': ((44, 25, 34), (8, 53, 19)),
    'Millau': ((44, 5, 14), (3, 1, 15)),
    'Golden Gate': ((37, 49, 11), (-122, -28, -43))
}

# Chemins vers les fichiers TIFF des bandes
ponts = {
    'Genes': {  'B02': 'img/Genes/2022-04-16-00_00_2022-04-16-23_59_Sentinel-2_L2A_B02_(Raw).tiff',
                'B03': 'img/Genes/2022-04-16-00_00_2022-04-16-23_59_Sentinel-2_L2A_B03_(Raw).tiff',
                'B04': 'img/Genes/2022-04-16-00_00_2022-04-16-23_59_Sentinel-2_L2A_B04_(Raw).tiff'},
    'Millau': { 'B02': 'img/Millau/2024-05-11-00_00_2024-05-11-23_59_Sentinel-2_L2A_B02_(Raw).tiff',    
                'B03': 'img/Millau/2024-05-11-00_00_2024-05-11-23_59_Sentinel-2_L2A_B03_(Raw).tiff',
                'B04': 'img/Millau/2024-05-11-00_00_2024-05-11-23_59_Sentinel-2_L2A_B04_(Raw).tiff'},
    'Golden Gate': {   'B02': 'img/Golden_Gates/2024-05-23-00_00_2024-05-23-23_59_Sentinel-2_L2A_B02_(Raw).tiff',
                        'B03': 'img/Golden_Gates/2024-05-23-00_00_2024-05-23-23_59_Sentinel-2_L2A_B03_(Raw).tiff',
                        'B04': 'img/Golden_Gates/2024-05-23-00_00_2024-05-23-23_59_Sentinel-2_L2A_B04_(Raw).tiff'}
}

def generation_carre(ville):

    if ville not in ponts.keys():
        print("Sujet non-inclue dans la base de donnée")
    else:
        # Ouverture des bandes bleue, verte et rouge pour la ville concernée
        B = gdal.Open(ponts[ville]['B02'])
        G = gdal.Open(ponts[ville]['B03'])
        R = gdal.Open(ponts[ville]['B04'])

        # Acquisition de la fonction faisant correspondre des coordonnées à un pixel
        transform = B.GetGeoTransform()

        # Conversion des coordonnées polaires en coordonnées web Mercator
        x, y = degrees2mercator(coords[ville][0], coords[ville][1])

        # Acquisition des indices des pixels extrêmes haut du carré de 2km de côté
        topleft = geo_to_pixel(transform, x - 1000, y + 1000)
        topright = geo_to_pixel(transform, x + 1000, y + 1000)


        side = topright[0] - topleft[0]


        # Extraction des bandes en tant qu'array sur la zone du carré de 2km de côté
        blue = B.GetRasterBand(1).ReadAsArray(topleft[0], topleft[1], side, side)
        green = G.GetRasterBand(1).ReadAsArray(topleft[0], topleft[1], side, side)
        red = R.GetRasterBand(1).ReadAsArray(topleft[0], topleft[1], side, side)

        #Normalisation des intensités des pixels
        red = normalize(red)
        green = normalize(green)
        blue = normalize(blue)

        # Étalement de l'histogramme des intensités des pixels pour augmenter le contraste
        red_eq = stretch_histogram(red)
        green_eq = stretch_histogram(green)
        blue_eq = stretch_histogram(blue)



        # Empilement des bandes pour créer une image RGB
        rgb_eq = np.dstack((red_eq, green_eq, blue_eq))

        # Affichage du carré
        plt.imshow(rgb_eq)
        plt.title(ville)
        plt.show()


