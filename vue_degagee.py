#!/usr/bin/env python3

"""
exploration d'une image paresseuse avec un itérateur ligne par ligne
"""

from image import Image
from imagep import ImageParesseuse
from algos import exploration, animer, raw_iterator, vue_degagee
from utils import limitation_memoire, priority_index


def main():
    """
    creation d'une image aleatoire avec 30% de chance que chaque pixel
    soit noir puis on explore a l'aide d'une pile en generant une animation.
    """

    """
    Itérateur ligne par ligne
    """
    img = Image.aleatoire(256, 30)
    img.sauvegarde("image_paresseuse_row_iterator")
    img = ImageParesseuse("image_paresseuse_row_iterator")
    iterator_raw = raw_iterator(img)
    vue_degagee(img, iterator_raw)
    print(img.bloc.cache_info())

    """
    Itérateur bloc par bloc
    """

if __name__ == "__main__":
    main()
