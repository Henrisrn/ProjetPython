import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import statistics
data = pd.read_excel("sampled_data.xlsx")

# Suppression des lignes avec des valeurs manquantes
data.dropna(subset=['Valeur fonciere', 'Code type local','Code commune'], inplace=True)

# Filtrer la dataframe en fonction d'une colonne ou d'une catégorie prédéfinie
def filter_data(data, column, value):
    filtered_data = data[data[column] == value]
    return filtered_data



# Suppression des valeurs extrêmes en utilisant les percentiles
def remove_outliers(data, column, lower_percentile, upper_percentile):
    lower_bound = data[column].quantile(lower_percentile)
    upper_bound = data[column].quantile(upper_percentile)
    
    data = data[(data[column] > lower_bound) & (data[column] < upper_bound)]
    return data

# Liste des colonnes pour lesquelles supprimer les valeurs extrêmes
columns_to_check = ['Surface reelle bati']

# Suppression des valeurs extrêmes pour chaque colonne
lower_percentile = 0.01
upper_percentile = 0.99

for column in columns_to_check:
    data = remove_outliers(data, column, lower_percentile, upper_percentile)


print(data)
data["PrixFloat"] = data["Valeur fonciere"].astype(float).fillna(0)
data["PrixInt"] = data["PrixFloat"].astype(int)
data["Surface terrain"] = data["Surface terrain"].astype(float)


#TEST DE GRAPH
departement = [75,78,92]
data["Prix/m2"] = data["PrixInt"]/data["Surface terrain"]
for j in departement:
    dept_data = data[data['Code departement'] == int(j)]
    type_counts = dept_data["Type local"].value_counts()
    type_counts_dict = type_counts.to_dict()
    fig, ax = plt.subplots()
    prixenfonctiondulocal = {}
    for u in type_counts_dict.keys():
        dept_datatype = dept_data[dept_data['Type local'] == str(u)]
        prixenfonctiondulocal[u] = dept_datatype["Prix/m2"].median()
    print(prixenfonctiondulocal)
    ax.barh(list(type_counts_dict.keys()), list(type_counts_dict.values()))
    ax.set_xlabel("Nombre d'occurrences")
    ax.set_ylabel("Type")
    ax.set_title("Type de local dans le département numéro : "+str(j))
    plt.show()
    fig, ax = plt.subplots()
    ax.barh(list(prixenfonctiondulocal.keys()), list(prixenfonctiondulocal.values()))
    ax.set_xlabel("Nombre d'occurrences")
    ax.set_ylabel("Type")
    ax.set_title("Prix/m² en fonction du type de local dans le département numéro : "+str(j))
    plt.show()