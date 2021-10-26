"""
les algorithmes un peu costauds sont ici
"""
from itertools import takewhile, chain
from os import system
import tempfile
from utils import voisins, compte, priority_index
import heapq


def animer(image, etapes, fichier="animation.gif", pas=100):
    """
    genere un fichier
    montrant l'evolution de l'image toutes les 'pas' 'etapes'
    """
    image_dir = tempfile.TemporaryDirectory()
    compte_images = 0
    image.pbm("{}/{:07d}.pbm".format(image_dir.name, compte_images))
    compte_images += 1

    for numero_etape, _ in enumerate(etapes):
        if numero_etape % pas == 0:
            image.pbm("{}/{:07d}.pbm".format(image_dir.name, compte_images))
            compte_images += 1

    image.pbm("{}/{:07d}.pbm".format(image_dir.name, compte_images))
    compte_images += 1
    if system("convert -delay 10 -loop 1 {}/*.pbm {}".format(image_dir.name, fichier)):
        print("echec de la creation du gif.\
image magick (convert) est-il installe ?")


def exploration(image):
    """
    exploration (et modification)
    de l'image en profondeur d'abord,
    a l'aide d'une pile.
    on yield a chaque etape la pile.
    """
    def pixel_blanc(p):
        return not image.pixel(*p)

    a_voir = [(0, 0)]
    while a_voir:
        courant = a_voir.pop()
        if pixel_blanc(courant):
            image.noircir_pixel(*courant)
            yield a_voir
            a_voir.extend(filter(pixel_blanc, voisins(image.taille, courant)))


def exploration_tas(image):
    """
    exploration (et modification)
    de l'image en profondeur,
    a l'aide d'un tas.
    on yield a chaque etape le tas.
    """
    def pixel_blanc(p):
        return not image.pixel(*p)

    a_voir = [(0, 0)]
    heapq.heapify(a_voir)
    while a_voir:
        courant = heapq.heappop(a_voir)
        if pixel_blanc(courant):
            image.noircir_pixel(*courant)
            yield a_voir
            for voisin in filter(pixel_blanc, voisins(image.taille, courant)):
                heapq.heappush(a_voir, voisin)


def exploration_priority(image):
    """
    exploration (et modification)
    de l'image en fonction des priorités,
    a l'aide d'un tas.
    on yield a chaque etape le tas.
    """
    def pixel_blanc(p):
        return not image.pixel(*p)

    a_voir = [(0, 0)]
    while a_voir:
        courant = a_voir.pop()
        if pixel_blanc(courant):
            image.noircir_pixel(*courant)
            yield a_voir
            a_voir.extend(filter(pixel_blanc, voisins(image.taille, courant)))
            a_voir.sort(key = priority_index, reverse = True)


def vue_degagee(image, iterateur_pixels):
    """
    renvoie la position avec la meilleure vue
    """
    def pixel_blanc(pixel):
        return not image.pixel(*pixel)

    def vue_pixel(pixel):
        def vision(pixels):
            return takewhile(pixel_blanc, pixels)
        ligne, colonne = pixel
        haut = vision((l, colonne) for l in reversed(range(0, ligne)))
        bas = vision((l, colonne) for l in range(ligne+1, image.taille))
        vertical = chain(haut, bas)

        gauche = vision((ligne, c) for c in reversed(range(0, colonne)))
        droite = vision((ligne, c) for c in range(colonne+1, image.taille))
        horizontal = chain(gauche, droite)

        return compte(chain(horizontal, vertical))
    return max(filter(pixel_blanc, iterateur_pixels), key=vue_pixel)


def raw_iterator(image):
    tab = []
    for i in range(image.taille):
        for j in range(image.taille):
            tab.append((i, j))
            yield (i, j)
    print(len(tab))


def bloc_iterator(image, K):
    nb_iter = image.taille / K
    for I in range(0, image.taille - K, K - 1):
        for J in range(0, image.taille - K, K - 1):
            for  i in range(I, I+K):
                for j in range(J, J+K):
                    yield (i, j)
