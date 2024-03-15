#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 11:16:20 2022

@author: antonomaz
"""

import numpy as np
from sklearn.cluster import AffinityPropagation
from sklearn.metrics import DistanceMetric 
from sklearn.feature_extraction.text import CountVectorizer
import sklearn
import json
import glob
import re
from collections import OrderedDict

# Fonction pour lire un fichier JSON et le charger en mémoire
def lire_fichier(chemin):
    with open(chemin) as json_data: 
        texte = json.load(json_data)
    return texte

# Fonction pour extraire le nom de fichier à partir du chemin complet
def nomfichier(chemin):
    nomfich = chemin.split("/")[-1].split(".")[0]
    return nomfich

chemin_entree = "json_pour_cluster"  # Chemin d'entrée contenant les fichiers JSON à traiter

# Parcourir tous les fichiers JSON dans le dossier d'entrée
for chemin_json in glob.glob(chemin_entree + "/*.json"):
    # Charger le contenu du fichier JSON
    liste = lire_fichier(chemin_json)

    # Initialiser un dictionnaire pour stocker les informations de sortie pour ce fichier JSON
    dic_output = {}

    dic_mots = {}
    i = 0

    # Compter la fréquence des mots dans la liste
    for mot in liste: 
        if mot not in dic_mots:
            dic_mots[mot] = 1
        else:
            dic_mots[mot] += 1
    
    # Trier le dictionnaire par ordre alphabétique des clés
    new_d = OrderedDict(sorted(dic_mots.items(), key=lambda t: t[0]))

    # Créer un ensemble des mots uniques dans la liste
    Set_00 = set(liste)
    Liste_00 = list(Set_00)
    liste_words = []
    matrice = []

    # Filtrer les mots pour ne conserver que ceux de longueur supérieure à 1
    for l in Liste_00:
        if len(l) != 1:
            liste_words.append(l)

    try:
        # Convertir la liste de mots en un tableau numpy
        words = np.asarray(liste_words)

        # Créer la matrice de similarité
        for w in words:
            liste_vecteur = []
            for w2 in words:
                V = CountVectorizer(ngram_range=(2, 3), analyzer='char')
                X = V.fit_transform([w, w2]).toarray()
                distance_tab1 = sklearn.metrics.pairwise.cosine_distances(X)
                liste_vecteur.append(distance_tab1[0][1])
            matrice.append(liste_vecteur)
        matrice_def = -1 * np.array(matrice)

        # Effectuer le clustering avec Affinity Propagation
        affprop = AffinityPropagation(affinity="precomputed", damping=0.6, random_state=None) 
        affprop.fit(matrice_def)
        
        # Traiter les clusters
        for cluster_id in np.unique(affprop.labels_):
            exemplar = words[affprop.cluster_centers_indices_[cluster_id]]
            cluster = np.unique(words[np.nonzero(affprop.labels_==cluster_id)])
            cluster_str = ", ".join(cluster)
            cluster_list = cluster_str.split(", ")

            Id = "ID " + str(i)
            for cle, dic in new_d.items(): 
                if cle == exemplar:
                    dic_output[Id] = {}
                    dic_output[Id]["Centroïde"] = exemplar
                    dic_output[Id]["Freq. centroide"] = dic
                    dic_output[Id]["Termes"] = cluster_list
                
            i = i + 1

    except:        
        print("**********Non OK***********", chemin_json)

    # Créer le nom du fichier de sortie en utilisant le nom du fichier d'entrée
    nom_sortie_json = nomfichier(chemin_json) + "_clusters.json"

    # Enregistrer les informations de sortie dans un fichier JSON séparé pour chaque fichier d'entrée
    with open(nom_sortie_json, "w", encoding="utf-8") as fichier_sortie:
        json.dump(dic_output, fichier_sortie, indent=4, ensure_ascii=False)

    print("Les clusters ont été enregistrés avec succès dans", nom_sortie_json)
