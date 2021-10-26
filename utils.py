"""
fonctions utilitaires mineures
"""

from math import ceil, sqrt
import os
import resource
from itertools import product
from random import randint
import psutil

INUTILE = None


def limitation_memoire():
    """
    limite fortement la memoire pour le reste de l'execution
    """
    conso = psutil.Process(os.getpid()).memory_info().vms
    resource.setrlimit(resource.RLIMIT_AS, (conso, conso))
    # on mange un peu de ce que python a pre-alloue
    # pour corser encore un peu la donne
    global INUTILE
    INUTILE = list(range(5000))


def bits(nombre, nombre_bits=8):
    """
    itere sur tous les bits du nombre, de taille 'nombre_bits'
    """
    for _ in range(nombre_bits):
        bit = nombre & 1
        nombre >>= 1
        yield bit


def octet_aleatoire(proba):
    """
    renvoie un octet aleatoire avec proba/100 chance
    pour chaque bit d'etre vrai
    """
    octet = 0
    for pos in range(8):
        if randint(1, 100) <= proba:
            octet |= (1 << pos)
    return octet


def inversion_bits(octet):
    """
    invers l'ordre des bits de l'octet
    """
    octet = (octet & 0xf0) >> 4 | (octet & 0x0f) << 4
    octet = (octet & 0xcc) >> 2 | (octet & 0x33) << 2
    octet = (octet & 0xaa) >> 1 | (octet & 0x55) << 1
    return octet


def voisins(limite, position):
    """
    itere sur les au plus 4 positions voisines de la position donnee.
    """
    ligne, colonne = position
    if ligne > 0:
        yield ligne - 1, colonne
    if ligne < limite - 1:
        yield ligne + 1, colonne
    if colonne > 0:
        yield ligne, colonne - 1
    if colonne < limite - 1:
        yield ligne, colonne + 1


def compte(iterateur):
    """
    consomme l'iterateur et renvoie son nombre d'elements
    """
    return sum(1 for _ in iterateur)


def pixels(image):
    """
    itere sur tous les indices valides de pixels d'un labyrinthe
    """
    return product(range(image.taille), range(image.taille))


def derouler(iterateur):
    """
    passe sur l'iterateur donne
    """
    for _ in iterateur:
        pass


def calcul_taille(nom_fichier):
    """
    retourne le n correspondant a l'image n x n dans le fichier donne
    """
    taille_fichier = os.path.getsize(nom_fichier)
    assert taille_fichier > 0
    nombre_lignes = ceil(sqrt(taille_fichier * 8))
    assert nombre_lignes * nombre_lignes == taille_fichier * 8
    return nombre_lignes

def priority_index(pixel):
    x = bits(pixel[0])
    y = bits(pixel[1])
    result = 0
    i = 0
    while (i < 15):
        result += next(x) * (2 ** i) + next(y) * (2 ** (i + 1))
        i += 2
    return result
