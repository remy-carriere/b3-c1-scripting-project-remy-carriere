"""
Script Python permettant de récupérer un fichier nommé conso-annuelles_v1.csv,
ayant pour colonnes ["Appareil suivi","ID logement","Consommation annuelle AN1", "Consommation annuelle AN2", "Type"]
enlever toutes les lignes contenant une case vide,
supprimer la colonne ID logement,
additionner les colonnes "Consommation annuelle" entre elles,
et rendre le résultat dans un fichier nommé conso-clean.csv
"""

import re
import pandas as pd
import csv

'''
J'ai fait le choix de ne pas utiliser de fonctions car ce script
se base sur des boucles imbriquées dans d'autres boucles,
et faire appel à des fonctions prend du temps sur l'exécution.
Je considère que ce n'était pas nécessaire pour un script de cette taille.
'''

df = pd.read_csv('conso-annuelles_v1.csv', sep=';', encoding='latin-1')

# Permet d'enlever les lignes avec une case vide
df_no_void = df.dropna()

# Dictionnaire permettant d'initialiser un Dataframe
# qui correspond aux lignes non-vides, et après vérification
# des formats de consommation annuelle.
data_added = {
    df.columns[0]: [],
    "Consommation annuelle": [],
    df.columns[4]: []
}

# Correspond aux lignes brutes du Dataframe, ce qui nous permet de les compter
index = df_no_void.index

for i in range(1, len(index)):

    # ----------------------------- VERIFICATION FORMAT DONNEES------------------------------
    # Si les cellules ne contiennent pas uniquement des caractères numériques et une virgule,
    # on le change en un 0 pour ne pas fausser les calculs, sinon on les cast en float en remplacant la virgule
    # par un point pour que Python puisse caster correctement
    if re.search("([0-9+,])\w+", str(df_no_void.loc[index[i]][2])) is None:
        first_el = 0
    else:
        if isinstance(df_no_void.loc[index[i]][2], str):
            first_el = float(str.replace(df_no_void.loc[index[i]][2], ",", "."))
        else:
            first_el = df_no_void.loc[index[i]][2]
    if re.search("([0-9+,])\w+", str(df_no_void.loc[index[i]][3])) is None:
        second_el = 0
    else:
        if isinstance(df_no_void.loc[index[i]][3], str):
            second_el = float(str.replace(df_no_void.loc[index[i]][3], ",", "."))
        else:
            second_el = df_no_void.loc[index[i]][3]

    # -------------------------------- SET VALEURS---------------------------------------
    # On ajoute les 2 consommations ensemble et on le rentre dans la case correspondante
    data_added[df_no_void.columns[0]].append(df_no_void.loc[index[i]][0])
    conso = round(first_el + second_el, 1)
    data_added["Consommation annuelle"].append(conso)
    data_added[df_no_void.columns[4]].append(df_no_void.loc[index[i]][4])

# On traduit ce dictionnaire en un Dataframe
df_added = pd.DataFrame(data_added)

# Que l'on rentre dans un fichier CSV
df_added.to_csv('intermediaire.csv', sep=';', encoding='latin-1')

# On utilise un fichier intermédiaire CSV pour faciliter le tri avec des listes
# plutôt qu'avec des DataFrames (selon les consignes, tri interdit via pandas).
with open("intermediaire.csv", 'r', encoding="latin-1") as inter_input:
    inter_list = []
    r = csv.reader(inter_input, delimiter=";")

    with open("conso-clean.csv", "w", newline="", encoding="latin-1") as conso_clean:
        w = csv.writer(conso_clean, delimiter=";")
        for line in r:
            inter_list.append(line)

        # On ajoute la première ligne avec les noms des colonnes
        # En enlevant la colonne d'identifiants ajoutée par pandas avec [1:]
        w.writerow(inter_list[0][1:])
        for line in sorted(inter_list[1:len(inter_list)], key=lambda row: (row[3], -float(row[2]))):
            # Puis on ajoute le reste, déjà trié
            # En enlevant la colonne d'identifiants ajoutée par pandas avec [1:]
            w.writerow(line[1:])

        print("Nombres de lignes total :" + str(len(inter_list)))
