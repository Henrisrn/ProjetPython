import pandas as pd
from django.shortcuts import render
import base64
from dash import html, dcc
from django_plotly_dash import DjangoDash
from io import BytesIO
import numpy as np
import geopandas as gpd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from urllib.request import urlopen
import json
import plotly.express as px
import datetime
#data = pd.read_csv("C://Users//henri//Projet_ESILV_A3//ProjetPython//monprojet//monprojet//valeursfoncieres-2022.txt", sep="|")
#data.drop(['Identifiant de document', 'Reference document', '1 Articles CGI', '2 Articles CGI', '3 Articles CGI', '4 Articles CGI', '5 Articles CGI', 'No disposition'], axis=1, inplace=True)
#data = pd.read_excel("C://Users//henri//Projet_ESILV_A3//ProjetPython//sampled_data.xlsx")

data = pd.read_csv("C://Users//henri//Downloads//valeursfoncieres-2021.txt",sep="|").sample(10000)
data.drop(['Identifiant de document', 'Reference document', '1 Articles CGI', '2 Articles CGI', '3 Articles CGI', '4 Articles CGI', '5 Articles CGI', 'No disposition'], axis=1, inplace=True)
data["Surface terrain"] = data["Surface terrain"].apply(lambda x: str(x).replace(',', '.'))
data["Valeur fonciere"] = data["Valeur fonciere"].apply(lambda x: str(x).replace(',', '.'))
data["Surface terrain"] = data["Surface terrain"].replace('', np.nan)
data["Type local"] = data["Type local"].replace('', np.nan)
data["Type de voie"] = data["Type de voie"].replace('', np.nan)
data = data.dropna(subset=["Surface terrain", "Type local", "Type de voie"], how='all')
data["Section"] = data["Section"].astype(str)
surfaceterrain = data["Surface terrain"].dropna()
surfaceterrain = surfaceterrain.astype(float)
valeurfonciere = data["Valeur fonciere"].dropna()
valeurfonciere = valeurfonciere.astype(float)
data["PrixFloat"] = data["Valeur fonciere"].astype(float).fillna(0)
data["PrixInt"] = data["PrixFloat"].astype(int)
data["Surface terrain"] = data["Surface terrain"].astype(float)
date = pd.to_datetime(data['Date mutation'], format="%d/%m/%Y")
month = date.dt.month
data["Date"] = date
data["Month"] = month
data["Days"] = date.dt.day
print(data)
def page2(request):
    #TEST DE GRAPH SYMPA
    # Embed plots into HTML via Flask Render
    
    scatter_plot = px.scatter(data, x="Surface terrain", y="PrixInt",
                          title="Nuage de points", labels={"x": "Valeur X", "y": "Valeur Y"})

    #-scatter_plot.show()
    url_geojson = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements-version-simplifiee.geojson"
    with urlopen(url_geojson) as response:
            geo_json_data = json.loads(response.read().decode())
    gdf = gpd.read_file(url_geojson)

    # Choropleth map
    mean_valeur_fonciere = data.groupby('Code departement')['PrixInt'].mean().reset_index()
    mean_valeur_fonciere.columns = ['code', 'valeur_fonciere_moyenne']

    choropleth_map = px.choropleth(mean_valeur_fonciere, geojson=geo_json_data, locations='code', color='valeur_fonciere_moyenne',
                                featureidkey="properties.code",
                                hover_name="valeur_fonciere_moyenne",
                                color_continuous_scale=px.colors.sequential.YlGn,
                                projection="mercator",
                                title="Valeur foncière moyenne par département",
                                labels={'valeur_fonciere_moyenne': 'Valeur foncière moyenne'})
    choropleth_map.update_geos(fitbounds="locations")
    choropleth_map.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
    count_ventes = data.groupby('Code departement').size().reset_index()
    count_ventes.columns = ['code', 'nombre_ventes']

    # Créer une carte centrée sur la France avec un fond de carte OpenStreetMap


    # Afficher la carte

    
    
    columns = ["Nature mutation", "Code type local", "Nombre pieces principales"]
    subplot_titles = [f'Histogramme {column}' for column in columns]

    # Créez un objet de sous-tracés avec 3 sous-tracés verticaux
    fig = make_subplots(rows=3, cols=1, subplot_titles=subplot_titles)

    # Ajoutez des histogrammes pour chaque colonne
    for i, column in enumerate(columns):
        fig.add_trace(go.Histogram(x=data[column].dropna(), nbinsx=30, name=column), row=i+1, col=1)

    # Mettez à jour les axes et le titre
    fig.update_layout(height=1500, width=1300)
    fig.update_xaxes(title_text=columns[0], row=1, col=1)
    fig.update_xaxes(title_text=columns[1], row=2, col=1)
    fig.update_xaxes(title_text=columns[2], row=3, col=1)
    fig.update_yaxes(title_text='Fréquence')


    fig2 = px.choropleth(
    count_ventes,
    geojson=geo_json_data,
    locations='code',
    featureidkey="properties.code",
    color='nombre_ventes',
    color_continuous_scale="BuGn",
    title="Nombre de ventes par département",
    labels={'nombre_ventes': 'Nombre de ventes'}
    )

    # Mise à jour des paramètres du graphique
    fig2.update_geos(fitbounds="locations")
    fig2.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        
    #fig.show()
    #choropleth_map.show()


        #EXPORT DES GRAPHS

            
        # Générer le code HTML
        # Générer le code HTML

    

    data["Date mutation"] = pd.to_datetime(data["Date mutation"], format="%d/%m/%Y")

    # Créer une colonne "Mois" qui contient le mois de chaque vente
    data["Mois"] = data["Date mutation"].dt.month

    # Calculer le prix médian des ventes pour chaque mois de l'année
    prix_median = data.groupby("Mois")["Valeur fonciere"].median()

    # Créez un DataFrame à partir des données prétraitées
    prix_median_df = pd.DataFrame({'Mois': prix_median.index, 'Prix médian': prix_median.values})

    # Créez le graphique de ligne avec Plotly Express
    fig4 = px.line(
        prix_median_df,
        x='Mois',
        y='Prix médian',
        title="Évolution du prix médian des ventes par mois en 2022",
        labels={'Mois': "Mois de l'année", 'Prix médian': 'Prix médian des ventes'}
    )
    
    nature_culture_counts = data["Nature culture"].value_counts().reset_index()
    nature_culture_counts.columns = ['Nature culture', 'Count']

    # Créez le graphique camembert avec Plotly Express
    fig5 = px.pie(
        nature_culture_counts,
        values='Count',
        names='Nature culture',
        title="Répartition des types de culture des terrains"
    )
    
    type_local_counts = data["Type local"].value_counts().reset_index()
    type_local_counts.columns = ['Type local', 'Count']

    # Créez le graphique camembert avec Plotly Express
    fig6 = px.pie(
        type_local_counts,
        values='Count',
        names='Type local',
        title="Répartition des types locaux des biens"
    )

    # %%
    # Convertir 'Date mutation' en datetime
    data['Date mutation'] = pd.to_datetime(data['Date mutation'], format='%d/%m/%Y')
    data['Date mutation'] = pd.to_datetime(data['Date mutation'], format='%d/%m/%Y')

    # Ajouter la colonne 'Mois'
    data['Mois'] = data['Date mutation'].dt.month
    data['Mois'] = data['Date mutation'].dt.month

    # Calculer l'IQR pour 'Valeur fonciere' dans les deux jeux de données
    Q1_1 = data['PrixFloat'].quantile(0.25)
    Q3_1 = data['PrixFloat'].quantile(0.75)
    IQR_1 = Q3_1 - Q1_1

    Q1_2 = data['PrixFloat'].quantile(0.25)
    Q3_2 = data['PrixFloat'].quantile(0.75)
    IQR_2 = Q3_2 - Q1_2

    # Définir les limites pour les valeurs aberrantes dans les deux jeux de données
    limite_inferieure_1 = Q1_1 - 1.5 * IQR_1
    limite_superieure_1 = Q3_1 + 1.5 * IQR_1

    limite_inferieure_2 = Q1_2 - 1.5 * IQR_2
    limite_superieure_2 = Q3_2 + 1.5 * IQR_2

    # Filtrer les données
    donnees_filtrees_1 = data[(data['PrixFloat'] >= limite_inferieure_1) & (data['PrixFloat'] <= limite_superieure_1)]
    donnees_filtrees_2 = data[(data['PrixFloat'] >= limite_inferieure_2) & (data['PrixFloat'] <= limite_superieure_2)]



    # Convertir 'Date mutation' en datetime
    # Votre code ici...

    # Boîte à moustaches pour la première année
    fig7 = px.box(donnees_filtrees_1, x='Mois', y='PrixFloat', title='Boîte à moustaches de "Valeur fonciere" par mois (valeurs aberrantes supprimées) - Année 1')

    # Boîte à moustaches pour la deuxième année
    fig8 = px.box(donnees_filtrees_2, x='Mois', y='PrixFloat', title='Boîte à moustaches de "Valeur fonciere" par mois (valeurs aberrantes supprimées) - Année 2')
    donnees_filtrees = pd.concat([donnees_filtrees_1, donnees_filtrees_2])

    # Créer une nouvelle colonne 'Année' dans les données filtrées
    donnees_filtrees['Annee'] = donnees_filtrees['Date mutation'].dt.year
    # Boîte à moustaches pour les deux années superposées
    fig9 = px.box(donnees_filtrees, x='Mois', y='PrixFloat', color='Annee', title='Boîte à moustaches de "Valeur fonciere" par mois (valeurs aberrantes supprimées), superposition des années')
    # Diagramme en barres du Nombre de Pièces Principales
    fig10 = px.histogram(data, x='Nombre pieces principales', nbins=int(max(data['Nombre pieces principales'].fillna(0))), title='Nombre de propriétés par nombre de pièces principales en 2022', color_discrete_sequence=['blue'])


    
    data['Nombre pieces principales'].value_counts().sort_index().plot(kind='bar', color='blue', alpha=0.5, label="2022")

   

    
    data['Type local'].value_counts().plot(kind='pie', autopct='%1.1f%%')
    data['Date mutation'] = pd.to_datetime(data['Date mutation'], format='%d/%m/%Y')
    # Diagramme en Camembert du Type Local
    fig12 = px.pie(data, names='Type local', title='Répartition des types de locaux en 2022')


    # Calcule l'IQR pour 'Surface reelle bati'
    Q1 = data['Surface reelle bati'].quantile(0.25)
    Q3 = data['Surface reelle bati'].quantile(0.75)
    IQR = Q3 - Q1

    # Définis les limites pour les valeurs aberrantes
    limite_inférieure = Q1 - 1.5 * IQR
    limite_supérieure = Q3 + 1.5 * IQR

    # Filtre les données
    data_filtrée = data[(data['Surface reelle bati'] >= limite_inférieure) & (data['Surface reelle bati'] <= limite_supérieure)]

    # Extrait le mois de la colonne 'Date mutation'
    data_filtrée['Mois'] = data_filtrée['Date mutation'].dt.month
    
    fig13 = px.pie(data, names='Type local', title='Répartition des types de locaux en 2019')

    data['Date mutation'] = pd.to_datetime(data['Date mutation'], format='%d/%m/%Y')
    # Diagramme en boîte pour "Surface reelle bati" par mois
    fig14 = px.box(data_filtrée, x='Mois', y='Surface reelle bati', title='Diagramme en boîte de "Surface Reelle Bati" par Mois (valeurs aberrantes enlevées)')


    # Calcule l'IQR pour 'Surface reelle bati'
    Q1 = data['Surface reelle bati'].quantile(0.25)
    Q3 = data['Surface reelle bati'].quantile(0.75)
    IQR = Q3 - Q1

    # Définis les limites pour les valeurs aberrantes
    limite_inférieure = Q1 - 1.5 * IQR
    limite_supérieure = Q3 + 1.5 * IQR

    # Filtre les données
    data_filtrée = data[(data['Surface reelle bati'] >= limite_inférieure) & (data['Surface reelle bati'] <= limite_supérieure)]

    # Extrait le mois de la colonne 'Date mutation'
    data_filtrée['Mois'] = data_filtrée['Date mutation'].dt.month

    
    fig15 = px.box(donnees_filtrees_1, x='Mois', y='Valeur fonciere', 
               title='Boîte à moustaches de "Valeur fonciere" par mois (valeurs aberrantes supprimées) - Année 1')


    # Boîte à moustaches pour la deuxième année
    fig16 = px.box(donnees_filtrees_2, x='Mois', y='Valeur fonciere',
                title='Boîte à moustaches de "Valeur fonciere" par mois (valeurs aberrantes supprimées) - Année 2')


    # Boîte à moustaches superposition des années
    fig17 = px.box(donnees_filtrees, x='Mois', y='Valeur fonciere', color='Annee',
                title='Boîte à moustaches de "Valeur fonciere" par mois (valeurs aberrantes supprimées), superposition des années')


    # Pie chart du Type Local
    fig19 = px.pie(data, names='Type local',
                title='Répartition des types de locaux en 2022')


    fig20 = px.pie(data, names='Type local',
                title='Répartition des types de locaux en 2019')


    # Boîte à moustaches de "Surface Reelle Bati" par Mois (valeurs aberrantes enlevées)
    fig21 = px.box(data_filtrée, x='Mois', y='Surface reelle bati',
                title='Diagramme en boîte de "Surface Reelle Bati" par Mois (valeurs aberrantes enlevées)')

    
    app = DjangoDash('app', add_bootstrap_links=True)
    app.layout = html.Div([
    html.Div([
        dcc.Graph(id='graph1', figure=choropleth_map),
        dcc.Graph(id='graph2', figure=scatter_plot),
        dcc.Graph(id='graph3', figure=fig),
        dcc.Graph(id='graph4', figure=fig2),
        dcc.Graph(id='graph5', figure=fig4),
        dcc.Graph(id='graph6', figure=fig5),
        dcc.Graph(id='graph7', figure=fig6),
        dcc.Graph(id='graph3', figure=fig7),
        dcc.Graph(id='graph4', figure=fig8),
        dcc.Graph(id='graph5', figure=fig9),
        dcc.Graph(id='graph6', figure=fig10),
        dcc.Graph(id='graph8', figure=fig12),
        dcc.Graph(id='graph8', figure=fig13),
        dcc.Graph(id='graph10', figure=fig14),
        dcc.Graph(id='graph11', figure=fig15),
        dcc.Graph(id='graph12', figure=fig16),
        dcc.Graph(id='graph13', figure=fig17),
        dcc.Graph(id='graph15', figure=fig19),
        dcc.Graph(id='graph16', figure=fig20),
        dcc.Graph(id='graph17', figure=fig21),
        
    ]),
])


    return render(request, "C://Users//henri//Projet_ESILV_A3//ProjetPython//monprojet//monprojet//templates//index.html")

