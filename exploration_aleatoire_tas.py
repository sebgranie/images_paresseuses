#!/usr/bin/env python3

"""
exploration d'une image aleatoire avec un tas
"""

from image import Image
from algos import exploration, animer, exploration_tas
from utils import limitation_memoire, priority_index


def main():
    """
    creation d'une image aleatoire avec 30% de chance que chaque pixel
    soit noir puis on explore a l'aide d'une pile en generant une animation.
    """

    img = Image.aleatoire(256, 30)
    # limitation_mem oire()  # decommentez-moi pour voir si ca passe
    animer(img, exploration_tas(img), fichier="exploration_aleatoire_tas.gif")


if __name__ == "__main__":
    main()
