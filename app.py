from flask import Flask, render_template, request, send_file, flash, redirect
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import json
import os

app = Flask(__name__)
app.secret_key = os.urandom(12)  # Nécessaire pour utiliser flash

# Configuration de Selenium pour utiliser Chrome
options = Options()
options.add_argument("--headless")  # Exécuter Chrome en mode headless
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Initialiser le driver Selenium
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Page d'accueil avec le formulaire pour entrer l'URL
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Récupérer le nom du champion
        champion_name = request.form['name'].strip().lower().replace(" ", "")
        url = "https://universe.leagueoflegends.com/fr_FR/story/champion/" + champion_name
        
        # Exécuter le script de scraping pour récupérer le contenu de la div spécifiée
        try:
            # Initialiser le driver Selenium
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver.get(url)

            # Attendre que le contenu soit chargé (ajuster le temps si nécessaire)
            time.sleep(3)  # Attendre 3 secondes

            # Récupérer la div avec l'ID "CatchElement"
            try:
                div = driver.find_element(By.ID, "CatchElement")
                contenu_div = div.get_attribute('innerHTML')  # Obtenir le contenu HTML de la div

                # Nettoyer le contenu HTML avec BeautifulSoup
                soup = BeautifulSoup(contenu_div, 'html.parser')
                texte_propre = soup.get_text()  # Extraire le texte brut

                # Récupérer le nom du personnage depuis l'URL
                personnage = url.split('/')[-1]  # Récupérer le dernier mot de l'URL

                # Créer un dictionnaire pour stocker les nouvelles données
                new_entry = {
                    "personnage": personnage,
                    "biographie": texte_propre
                }

                # Tenter de lire les données existantes dans bio.json
                if os.path.exists("bio.json"):
                    with open("bio.json", "r", encoding="utf-8") as json_file:
                        try:
                            # Charger les données existantes
                            data = json.load(json_file)  
                        except json.JSONDecodeError:  # Gérer l'erreur si le fichier est vide ou mal formé
                            data = []  # Si le fichier est vide, initialiser une liste vide
                else:
                    data = []  # Si le fichier n'existe pas, initialiser une liste vide

                # Vérifier que data est une liste
                if not isinstance(data, list):
                    data = []  # Assurer que data est une liste

                # Ajouter la nouvelle entrée à la liste des données
                data.append(new_entry)

                # Écrire les données accumulées dans le fichier JSON
                with open("bio.json", "w", encoding="utf-8") as json_file:
                    json.dump(data, json_file, ensure_ascii=False, indent=4)
                
                flash('Chargement de données effectué. Téléchargement disponible')  # Message de succès

            except Exception as e:
                flash(f"Erreur lors de la récupération de la div : {str(e)}")

            driver.quit()  # Fermer le navigateur

        except Exception as e:
            flash(f"Une erreur est survenue : {str(e)}")
        
        return redirect('/')  # Rediriger vers la page principale pour afficher les messages flash

    return render_template('index.html', html_content=None)

@app.route('/download')
def download_file():
    # Vérifie si le fichier existe
    if os.path.exists("bio.json"):
        return send_file("bio.json", as_attachment=True)
    return "Fichier non trouvé", 404

if __name__ == '__main__':
    app.run(debug=True)
