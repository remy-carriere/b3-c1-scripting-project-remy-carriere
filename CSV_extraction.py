import re
import pandas as pd

df = pd.read_csv('conso-annuelles_v1.csv', sep=';', encoding='latin-1')

print(df.columns)
print("Nombres de lignes avant cleaning :" + str(len(df.index)))

df_no_void = df.dropna()
print("Nombres de lignes après cleaning :" + str(len(df_no_void.index)))

data_added = {
    df.columns[0]: [],
    df.columns[1]: [],
    "Consommation annuelle": [],
    df.columns[4]: []
}

print(df.loc[2][2])

index = df_no_void.index

for i in range(1, len(index)):
    #VERIFICATION FORMAT DONNEES
    if (str(df_no_void.loc[index[i]][2]) not in (None,"") and
            str(df_no_void.loc[index[i]][3]) not in (None,"")):
        if(re.search("([0-9+,])\w+", str(df_no_void.loc[index[i]][2])) == None):
            first_el = 0
        else:
            if (isinstance(df_no_void.loc[index[i]][2], str)):
                first_el = float(str.replace(df_no_void.loc[index[i]][2], ",", "."))
            else:
                first_el = df_no_void.loc[index[i]][2]
        if(re.search("([0-9+,])\w+", str(df_no_void.loc[index[i]][3])) == None):
            second_el = 0
        else:
            if (isinstance(df_no_void.loc[index[i]][3], str)):
                second_el = float(str.replace(df_no_void.loc[index[i]][3], ",", "."))
            else:
                second_el = df_no_void.loc[index[i]][3]
                
        #SET VALEURS
        data_added[df_no_void.columns[0]].append(df_no_void.loc[index[i]][0])
        data_added[df_no_void.columns[1]].append(df_no_void.loc[index[i]][1])
        conso = first_el + second_el
        data_added["Consommation annuelle"].append(conso)
        data_added[df_no_void.columns[4]].append(df_no_void.loc[index[i]][4])

df_added = pd.DataFrame(data_added)

print("Nombres de lignes total :" + str(len(df_added.index)))

df_ordered = df_added.sort_values(by=["Type","Consommation annuelle"],axis=0, ascending = [True, False])

df_ordered.to_csv('conso-clean.csv',sep=';',encoding='latin-1')
