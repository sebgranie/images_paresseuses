"""
une classe ImageParesseuse avec une conso memoire bornee
et une classe Bloc et son fonctionnement interne.
"""
from functools import lru_cache
from utils import calcul_taille


class Bloc:
    """
    Un bloc de donnees (correspond a une ligne de cache).
    """
    TAILLE = 32//8  # en octets

    def __init__(self, image, numero):
        self.depart = Bloc.TAILLE*numero
        image.fichier.seek(self.depart)
        self.octets = bytearray(image.fichier.read(Bloc.TAILLE))
        self.fichier = image.fichier
        self.changement = False

    def indices_octet_bit(self, indice):
        """
        prend un indice global de pixel et renvoie
        un indice local d'octet et de bit
        """
        assert self.depart*8 <= indice < (self.depart + Bloc.TAILLE)*8
        indice_local = indice - self.depart * 8
        indice_octet = indice_local // 8
        indice_bit = indice_local % 8
        return indice_octet, indice_bit

    def pixel(self, indice):
        """
        renvoie le pixel d'indice global donne
        """
        indice_octet, indice_bit = self.indices_octet_bit(indice)
        return self.octets[indice_octet] & (1 << indice_bit)

    def noircir_pixel(self, indice):
        """
        noircit le pixel d'indice global donne
        """
        indice_octet, indice_bit = self.indices_octet_bit(indice)
        self.octets[indice_octet] |= (1 << indice_bit)
        self.changement = True

    def __del__(self):
        """
        destruction d'un bloc
        avec flush des changements eventuels sur le disque
        """
        if self.changement:
            self.fichier.seek(self.depart)
            self.fichier.write(self.octets)


class ImageParesseuse:
    """
    Une image chargee paresseusement par blocs.
    Les blocs sont stockes dans un cache lru.
    """

    def __init__(self, nom_fichier):
        self.taille = calcul_taille(nom_fichier)
        self.fichier = open(nom_fichier, "r+b")

    def __del__(self):
        # on vide le cache pour forcer les ecritures eventuelles restantes
        self.bloc.cache_clear()

    @lru_cache(maxsize=256)
    def bloc(self, numero):
        """
        renvoie le bloc d'indice donne
        """
        return Bloc(self, numero)

    def indice_bloc_pixel(self, ligne, colonne):
        """
        etant donne la ligne et colonne d'un pixel
        renvoie son indice global et son bloc
        """
        indice = ligne * self.taille + colonne
        indice_octet = indice // 8
        indice_bloc = indice_octet // Bloc.TAILLE
        bloc_pixel = self.bloc(indice_bloc)
        return indice, bloc_pixel

    def pixel(self, ligne, colonne):
        """
        renvoie le pixel donne
        """
        indice, bloc_pixel = self.indice_bloc_pixel(ligne, colonne)
        return bloc_pixel.pixel(indice)

    def noircir_pixel(self, ligne, colonne):
        """
        noicit le pixel donne.
        les changements ne sont pas propages immediatement sur le disque.
        """
        indice, bloc_pixel = self.indice_bloc_pixel(ligne, colonne)
        bloc_pixel.noircir_pixel(indice)

    def pbm(self, nom_fichier):
        """
        ne fait rien (on n'affiche pas d'image)
        """
        ...
