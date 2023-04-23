import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render
import matplotlib.pyplot as plt
import base64
from io import BytesIO

def save_base64(fig):
    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    return base64.b64encode(image_png).decode('utf8')
def index(request):
    data = pd.read_csv("C://Users//henri//Projet_ESILV_A3//ProjetPython//monprojet//monprojet//valeursfoncieres-2022.txt", sep="|")
    echantillon = data[:1000]
    images = []
    data["Surface terrain"] = data["Surface terrain"].apply(lambda x: str(x).replace(',', '.'))
    data["Valeur fonciere"] = data["Valeur fonciere"].apply(lambda x: str(x).replace(',', '.'))

    data["Section"] = data["Section"].astype(str)
    surfaceterrain = data["Surface terrain"].dropna()
    surfaceterrain = surfaceterrain.astype(float)
    valeurfonciere = data["Valeur fonciere"].dropna()
    valeurfonciere = valeurfonciere.astype(float)

        # Histogramme
    fig1 = plt.figure(figsize=(6, 4))
    plt.hist(data["Section"], bins=30, alpha=0.75, color='blue')
    plt.xlabel('Valeur')
    plt.ylabel('Fréquence')
    plt.title('Histogramme')
    plt.grid(True)
    image_base64 = save_base64(fig1)
    images.append(image_base64)
    plt.close(fig1)
        
        # Nuage de points (scatter plot)
    fig1 = plt.figure(figsize=(6, 4))
    plt.scatter(surfaceterrain, valeurfonciere, alpha=0.75, color='green', edgecolors='black')
    plt.xlabel('Valeur X')
    plt.ylabel('Valeur Y')
    plt.title('Nuage de points')
    plt.grid(True)
    image_base64 = save_base64(fig1)
    images.append(image_base64)
    plt.close(fig1)

        # Nuage de points (scatter plot)
    fig1 = plt.figure(figsize=(6, 4))
    plt.plot(valeurfonciere, alpha=0.75, color='green')
    plt.xlabel('Valeur X')
    plt.ylabel('Valeur Y')
    plt.title('Nuage de points')
    plt.grid(True)
    image_base64 = save_base64(fig1)
    images.append(image_base64)
    plt.close(fig1)
    # Générer le code HTML
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Dataframe Echantillon et Graphiques</title>
    <style>
        img {{
            width: 100%;
            max-width: 300px;
        }}
    </style>
</head>
<body>
    <h1>Dataframe Echantillon</h1>
    <h2>Graphiques</h2>
    <div>
        {"".join([f'<img src="data:image/png;base64,{img}" />' for img in images])}
    </div>
</body>
</html>"""

    return HttpResponse(html)