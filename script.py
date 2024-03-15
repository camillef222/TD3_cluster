# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 16:20:19 2024

@author: user
"""

import json
import glob
import pandas as pd

def lire_fichier(chemin):
    with open(chemin, "r", encoding="utf-8") as f:
        contenu = f.read()
    return contenu

def extraire_entites_bio(chemin):
    contenu = lire_fichier(chemin)
    lignes = contenu.split("\n")
    entites = set()
    for ligne in lignes:
        if ligne.strip():  # Vérifie si la ligne n'est pas vide
            elements = ligne.split()
            if len(elements) >= 2:
                entite, bio = elements
                if bio.startswith(("B-", "I-")):
                    entites.add(entite)
    return entites


def nom_fichier(chemin):
    return chemin.split("\\")[-1].replace(".bio", "")

for chemin in glob.glob("DATA/*/*/*.bio"):
    entites = extraire_entites_bio(chemin)
    nom_fichier_json = f"entites_{nom_fichier(chemin)}.json"
    with open(nom_fichier_json, "w", encoding="utf-8") as f:
        json.dump(list(entites), f, indent=2, ensure_ascii=False)
