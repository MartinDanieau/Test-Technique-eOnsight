***Test Technique pour eOnsight***

Bienvenue sur ce répôt git !

Pour ce test technique, on cherche à générer une image carrée de 2km de côté, centré sur le viaduc Gênes-Saint-Georges, avec un bon niveau de contraste (qui peut s'apparenter à une image "True Color"), en se basant sur les images "Raw" produites par Sentinel-2. Pour aller plus loin, je suis allé chercher les images "Raw" incluant le viaduc de Millau et le Golden Gate Bridge sur https://apps.sentinel-hub.com/eo-browser/ et j'ai autonatisé le processus pour qu'il puisse s'appliquer de la même manière pour les 3 ponts.

**Bibliothèques et modules utilisés**

Pour ce test, j'ai utilisé GDAL (installé à partir d'un fichier wheel présent dans le répôt) pour la lecture des images GeoTiff, j'ai utilisé numpy pour traiter les tableau et le module pyplot de matplotlib pour afficher les images. J'utilise aussi le module math pour divers calculs.

*Versions utilsées*
Python 3.10.7
GDAL 3.8.4
numpy 1.23.3
matplotlib 3.6.0


**Principe**

Le fichier main.py contient la fonction generation_carre(ville) qui prend en argument une chaîne de caractères indiquant quel pont est le sujet de la fonction. Si la chaîne de caractère désigne un pont qui ne se trouve pas dans la base de donnée, la fonction renvoie "Sujet non-inclue dans la base de donnée" et s'arrête. Sinon, elle lit les bandes B02, B03 et B04 correspondantes, repère la zone à isoler et extrait les valeurs des différentes bandes en tant qu'array sur cette zone. Les composantes sont ensuite normalisées et la fonction étale leur histogramme de manière à obtenir un bon contraste. Enfin, la fonction crée l'image en couleur en réunissant les 3 composantes puis l'affiche.

Le fichier tools.py contient les différentes fonctions utiles au traitement des images :

- normalize(array) : prend en argument un array et le renvoie normalisé entre 0 et 255

- stretch_histogram(band_array, min_percent, max_percent) : prend en argument un array et les centiles inférieurs supérieur de son histogramme. Cette fonction étale dilate les valeurs comprisent entre les centiles extrêmes entre 0 et 255 et fixe à 0 les pixels du centile inférieur et à 255 les pixels du centile supérieur.

- geo_to_pixel(transform, geo_x, geo_y) : prend en argument une fonction faisant correspondre une coordonnée à un pixel, et des coordonnées web Mercator. Renvoie le pixel correspondant à une paire x, y de coordonnées de web Mercator.

- degrees2mercator(lat, lon): prend en argument 2 tuples représentant une latitude et une longitude en degrées, minutes, secondes et renvoie les coordonnées correspondantes au formant web Mercator
