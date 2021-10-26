"""
Images bitmaps
"""
from utils import octet_aleatoire, bits, inversion_bits, calcul_taille


class Image:
    """
    Une image noir/blanc relativement compressee
    (chaque ligne est codee par un bytearray)
    """

    def __init__(self, matrice):
        self.matrice = matrice
        self.taille = len(self.matrice)

    @classmethod
    def lecture(cls, fichier):
        """
        chargement d'une Image depuis un fichier
        """
        nombre_lignes = calcul_taille(fichier)
        with open(fichier, "rb") as graphe:
            matrice = [
                bytearray(graphe.read(nombre_lignes // 8))
                for _ in range(nombre_lignes)
            ]
        return cls(matrice)

    @classmethod
    def aleatoire(cls, taille, proba):
        """
        generation d'une image bruit.
        chaque pixel a proba/100 chances d'etre noir.
        """
        assert taille % 8 == 0
        matrice = [
            bytearray(octet_aleatoire(proba) for _ in range(taille // 8))
            for _ in range(taille)
        ]
        matrice[0][0] &= 254  # on efface le pixel 0,0

        return cls(matrice)

    def pixel(self, ligne, colonne):
        """
        renvoie le pixel a la position ligne, colonne
        """
        return self.matrice[ligne][colonne//8] & (1 << (colonne % 8))

    def noircir_pixel(self, ligne, colonne):
        """
        passe le pixel a la position ligne, colonne en noir
        """
        self.matrice[ligne][colonne//8] = self.matrice[ligne][colonne//8] | (1 << (colonne % 8))

    def blanchir_pixel(self, ligne, colonne):
        """
        passe le pixel a la position ligne, colonne en blanc
        """
        self.matrice[ligne][colonne//8] = self.matrice[ligne][colonne//8] & ~(1 << (colonne % 8))

    def sauvegarde(self, nom_fichier):
        """
        sauvegarde l'image dans le fichier donne
        """
        with open(nom_fichier, "wb") as image:
            for ligne in self.matrice:
                image.write(ligne)

    def affichage(self):
        """
        affiche l'image dans le terminal
        """
        for ligne in self.matrice:
            for octet in ligne:
                for bit in bits(octet):
                    print("#" if bit else " ", end="")
            print("")

    def pbm(self, nom_fichier):
        """
        sauvegarde l'image au format pbm (visualisable dans
        un visualiseur d'image)
        """
        with open(nom_fichier, "wb") as image:
            image.write(bytes("P4\n", "ascii"))
            image.write(bytes("{} {}\n".format(len(self.matrice), len(self.matrice)), "ascii"))
            for ligne in self.matrice:
                image.write(bytearray(inversion_bits(o) for o in ligne))
