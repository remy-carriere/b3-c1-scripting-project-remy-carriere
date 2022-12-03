import re
import pandas as pd
import csv

df = pd.read_csv('conso-annuelles_v1.csv', sep=';', encoding='latin-1')

# print(df.columns)
# print("Nombres de lignes avant cleaning :" + str(len(df.index)))

df_no_void = df.dropna()
# print("Nombres de lignes après cleaning :" + str(len(df_no_void.index)))

data_added = {
    df.columns[0]: [],
    "Consommation annuelle": [],
    df.columns[4]: []
}

index = df_no_void.index

for i in range(1, len(index)):
    # VERIFICATION FORMAT DONNEES
    # Si des cellules dans les colonnes 2 et 3 (Consommation) sont vides, on ne les utilise pas
    if (str(df_no_void.loc[index[i]][2]) not in (None, "") and
            str(df_no_void.loc[index[i]][3]) not in (None, "")):
        # Autrement, si ces cellules ne contiennent pas uniquement des caractères numériques et une virgule,
        # on le change en un 0 pour ne pas fausser les calculs, sinon on les cast en float en remplacant la virgule
        # par un point
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

        # SET VALEURS
        # On ajoute les 2 consommations ensemble et on le rentre dans la case correspondante
        data_added[df_no_void.columns[0]].append(df_no_void.loc[index[i]][0])
        conso = round(first_el + second_el, 1)
        data_added["Consommation annuelle"].append(conso)
        data_added[df_no_void.columns[4]].append(df_no_void.loc[index[i]][4])

df_added = pd.DataFrame(data_added)

df_added.to_csv('intermediaire.csv', sep=';', encoding='latin-1')

# On utilise un fichier intermédiaire CSV pour faciliter le tri avec des listes
# plutôt qu'avec des DataFrames (selon les consignes).
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
