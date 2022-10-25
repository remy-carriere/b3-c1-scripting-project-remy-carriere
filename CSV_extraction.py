import re
import pandas as pd

df = pd.read_csv('conso-annuelles_v1.csv', sep=';', encoding='latin-1')

data_added = {
    df.columns[0]: [],
    df.columns[1]: [],
    "Consommation annuelle": [],
    df.columns[4]: []
}

print(df.loc[2][2])

for i in range(1, len(df.index)):
    #VERIFICATION FORMAT DONNEES
    if (str(df.loc[i][2]) not in (None,"") and
            str(df.loc[i][3]) not in (None,"")):
        if(re.search("([0-9+,])\w+", str(df.loc[i][2])) == None):
            first_el = 0
        else:
            if (isinstance(df.loc[i][2], str)):
                first_el = float(str.replace(df.loc[i][2], ",", "."))
            else:
                first_el = df.loc[i][2]
        if(re.search("([0-9+,])\w+", str(df.loc[i][3])) == None):
            second_el = 0
        else:
            if (isinstance(df.loc[i][3], str)):
                second_el = float(str.replace(df.loc[i][3], ",", "."))
            else:
                second_el = df.loc[i][3]
                
        #SET VALEURS
        data_added[df.columns[0]].append(df.loc[i][0])
        data_added[df.columns[1]].append(df.loc[i][1])
        conso = first_el + second_el
        data_added["Consommation annuelle"].append(conso)
        data_added[df.columns[4]].append(df.loc[i][4])

df_added = pd.DataFrame(data_added)

print(df_added.columns)
print("Nombres de lignes avant cleaning :" + str(len(df_added.index)))

df_no_void = df_added.dropna()
print("Nombres de lignes après cleaning :" + str(len(df_no_void.index)))

# print("index df_no_void : "+ str(df_no_void.index))

print(df_no_void.loc[3][1])
print(df_no_void.loc[3])

df_no_void.to_csv('clean.csv',sep=';',encoding='latin-1')
