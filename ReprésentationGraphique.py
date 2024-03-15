# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 15:36:35 2024

@author: user
"""

import json
import glob
import matplotlib.pyplot as plt

# Chemin vers le dossier contenant les fichiers JSON pour le clustering
chemin_json_cluster = "cluster_pour_graphique"

# Parcourir tous les fichiers JSON dans le dossier
for chemin_json in glob.glob(chemin_json_cluster + "/*.json"):
    with open(chemin_json, "r", encoding="utf-8") as fichier_json:
        donnees = json.load(fichier_json)

        # Extraire les centroïdes et leurs fréquences pour chaque cluster
        centroïdes = [donnees[cluster]["Centroïde"] for cluster in donnees]
        freq_centroïdes = [donnees[cluster]["Freq. centroide"] for cluster in donnees]

        # Créer un graphique à barres pour visualiser les centroïdes et leurs fréquences
        plt.figure(figsize=(10, 6))
        plt.barh(centroïdes, freq_centroïdes, color='skyblue')
        plt.xlabel('Fréquence')
        plt.ylabel('Centroïdes')
        plt.title('Clustering des centroïdes')
        plt.gca().invert_yaxis()  # Inverser l'axe y pour afficher les plus fréquents en haut
        plt.tight_layout()

        # Enregistrer le graphique dans un fichier avec le même nom que le fichier JSON traité
        nom_fichier_graphique = chemin_json.replace(".json", "_graphique.png")
        plt.savefig(nom_fichier_graphique)

        # Afficher le chemin du fichier enregistré
        print(f"Le graphique a été enregistré avec succès sous {nom_fichier_graphique}")

        # Afficher le graphique
        plt.show()
