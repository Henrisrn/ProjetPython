import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import statistics
data = pd.read_csv("valeursfoncieres-2022.txt",sep="|")
data.drop(['Identifiant de document','Reference document','1 Articles CGI','2 Articles CGI','3 Articles CGI','4 Articles CGI','5 Articles CGI','No disposition'],axis=1, inplace=True)
# Conversion de la colonne 'Date mutation' au format date
data['Date mutation'] = pd.to_datetime(data['Date mutation'], format='%d/%m/%Y')

# Conversion de la colonne 'Valeur fonciere' au format float
data['Valeur fonciere'] = data['Valeur fonciere'].str.replace(',', '.').astype(float)
# Sélectionner un échantillon aléatoire de 1500 lignes
sampled_data = data.sample(n=5000)

# Exporter l'échantillon aléatoire dans un fichier Excel
sampled_data.to_excel('sampled_data.xlsx', index=False)