import re
import pandas as pd
import csv
from collections import defaultdict

df = pd.read_csv('conso-annuelles_v1.csv', sep=';', encoding='latin-1')

print(df.columns)
print("Nombres de lignes avant cleaning :" + str(len(df.index)))

df_no_void = df.dropna()
print("Nombres de lignes après cleaning :" + str(len(df_no_void.index)))

data_added = {
    df.columns[0]: [],
    "Consommation annuelle": [],
    df.columns[4]: []
}

number_of_elements = {}

print(df.loc[2][2])


index = df_no_void.index

for i in range(1, len(index)):
    # VERIFICATION FORMAT DONNEES
    if (str(df_no_void.loc[index[i]][2]) not in (None, "") and
            str(df_no_void.loc[index[i]][3]) not in (None, "")):
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
        data_added[df_no_void.columns[0]].append(df_no_void.loc[index[i]][0])
        conso = first_el + second_el
        data_added["Consommation annuelle"].append(conso)
        data_added[df_no_void.columns[4]].append(df_no_void.loc[index[i]][4])

df_added = pd.DataFrame(data_added)

print("Nombres de lignes total :" + str(len(df_added.index)))

index_added = df_added.index

# df_ordered = df_added.sort_values(by=["Type", "Consommation annuelle"], axis=0, ascending=[True, False])

# df_ordered.to_csv('conso-clean.csv', sep=';', encoding='latin-1')


df_added.to_csv('intermediaire.csv', sep=';', encoding='latin-1')

with open("intermediaire.csv",'r') as inter_input:
    #files = [open('input1','r')]
    counts = defaultdict(int)

    my_list = []
    r = csv.reader(inter_input, delimiter=";")

    with open("conso-clean.csv","w",newline="") as conso_clean:
        w = csv.writer(conso_clean,delimiter=";")
        for line in r:
            my_list.append(line)
        list_ordered = []
        list_ordered.append(my_list[0])
        for line in sorted(my_list[1:len(my_list)],key=lambda row: (row[3],float(row[2]))):
            list_ordered.append(line)
        # list_ordered = [my_list[0],]
        # print(list_ordered)

        for line in list_ordered:
            w.writerow(line)
    # for line in r:
    #     for num in line:
    #         counts[int(num)] += 1

    # with open('conso-clean.csv', mode='w') as employee_file:
    # for key,val in sorted(counts.items()):
    #     print (key, val)
