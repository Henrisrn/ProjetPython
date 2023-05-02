import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render
import matplotlib.pyplot as plt
import base64
from io import BytesIO
def generate_extra_charts(data):
    # Exemple: générer un histogramme pour "Nature mutation", "Code type local" et "Nombre pieces principales"
    extra_charts = []
    for column in ["Nature mutation", "Code type local", "Nombre pieces principales"]:
        fig = plt.figure(figsize=(6, 4))
        plt.hist(data[column].dropna(), bins=30, alpha=0.75)
        plt.xlabel(column)
        plt.ylabel('Fréquence')
        plt.title(f'Histogramme {column}')
        plt.grid(True)
        image_base64 = save_base64(fig)
        extra_charts.append(image_base64)
        plt.close(fig)

    return extra_charts

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
    print("bonjour")
    data["Section"] = data["Section"].astype(str)
    surfaceterrain = data["Surface terrain"].dropna()
    surfaceterrain = surfaceterrain.astype(float)
    valeurfonciere = data["Valeur fonciere"].dropna()
    valeurfonciere = valeurfonciere.astype(float)
    extra_charts = generate_extra_charts(data)
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
        body {{
            font-family: Arial, sans-serif;
            color: #333;
        }}
        img {{
            width: 100%;
            max-width: 300px;
        }}
        form {{
            margin-bottom: 2rem;
        }}
    </style>
</head>
<body>
    <h1>Dataframe Echantillon</h1>
    <h2>Graphiques</h2>
    <form method="post">
        <label for="categories">Sélectionnez une catégorie:</label>
        <select id="categories" name="categories">
            <option value="Identifiant de document">Identifiant de document</option>
            <!-- Ajoutez les autres options ici -->
        </select>
        <input type="submit" value="Mettre à jour">
    </form>
    <div>
        {"".join([f'<img src="data:image/png;base64,{img}" />' for img in images + extra_charts])}
    </div>
</body>
</html>"""

    return HttpResponse(html)
