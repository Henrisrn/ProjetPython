import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import statistics
data = pd.read_excel("sampled_data.xlsx")
fr_departments ={
    "Auvergne-Rhône-Alpes": ["1", "3", "7", "15", "26", "38", "42", "43", "63", "69", "73", "74"],
    "Bourgogne-Franche-Comté": ["21", "25", "39", "58", "70", "71", "89", "90"],
    "Bretagne": ["22", "29", "35", "56"],
    "Centre-Val de Loire": ["18", "28", "36", "37", "41", "45"],
    "Corse": ["2A", "2B"],
    "Grand Est": ["8", "10", "51", "52", "54", "55", "57", "67", "68", "88"],
    "Hauts-de-France": ["2", "59", "60", "62", "80"],
    "Île-de-France": ["75", "77", "78", "91", "92", "93", "94", "95"],
    "Normandie": ["14", "27", "50", "61", "76"],
    "Nouvelle-Aquitaine": ["16", "17", "19", "23", "24", "33", "40", "47", "64", "79", "86", "87"],
    "Occitanie": ["09", "11", "12", "30", "31", "32", "34", "46", "48", "65", "66", "81", "82"],
    "Pays de la Loire": ["44", "49", "53", "72", "85"],
    "Provence-Alpes-Côte d'Azur": ["4", "5", "6", "13", "83", "84"]
}
print(fr_departments)
data["Region"] = np.nan
for i in range(len(data["Code departement"])):
    valeurdepartement = data["Code departement"][i]
    for j in fr_departments:
        if(str(valeurdepartement) in fr_departments[j]):
            data["Region"][i] = j
            break
print(data["Region"])
data["Surface terrain"].dropna()
data['Prix/m2'] = data["Valeur fonciere"]/data["Surface terrain"]
data = data[data['Prix/m2'] > 1000]
data = data[data['Prix/m2'] < 20000]
#data.to_excel("SortieTraitement.xlsx")
