from flask import Flask, render_template, request, send_file
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

# Configuration de Selenium pour utiliser Chrome
options = Options()
#options.add_argument("--headless") 
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920x1080")

# Fonction pour initialiser le driver
def init_driver():
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        champion_name = request.form['name'].strip().lower().replace(" ", "").replace(".", "").replace("é", "e").replace("î", "i")
        url = "https://universe.leagueoflegends.com/fr_FR/story/champion/" + champion_name
        
        try:
            driver = init_driver()
            driver.get(url)

            # Attendre que le contenu soit chargé
            time.sleep(3)

            # Récupérer la div avec l'ID "CatchElement"
            div = driver.find_element(By.ID, "CatchElement")
            contenu_div = div.get_attribute('innerHTML')

            # Nettoyer le contenu HTML avec BeautifulSoup
            soup = BeautifulSoup(contenu_div, 'html.parser')
            texte_propre = soup.get_text()

            # Gérer le stockage des données dans bio.json
            personnage = url.split('/')[-1]
            new_entry = {"personnage": personnage, "biographie": texte_propre}

            # Tente de lire les données existantes dans bio.json
            if os.path.exists("bio.json"):
                with open("bio.json", "r", encoding="utf-8") as json_file:
                    try:
                        data = json.load(json_file)
                    except json.JSONDecodeError:
                        data = []
            else:
                data = []

            # Ajouter la nouvelle entrée à la liste des données
            data.append(new_entry)

            # Écrire les données accumulées dans le fichier JSON
            with open("bio.json", "w", encoding="utf-8") as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)

            driver.quit()

        except Exception as e:
            contenu_div = f"Une erreur est survenue : {str(e)}"

    return render_template('index.html', html_content=None)

@app.route('/launch')
def launch():
    try:
        # Lire le fichier JSON pour obtenir tous les noms des champions
        with open("champions.json", "r") as file:
            champions = json.load(file)

        driver = init_driver()
        for champion_name in champions:
            champion_name_clean = champion_name.strip().lower().replace(" ", "").replace("'", "").replace(".", "").replace("é", "e").replace("î", "i")
            url = f"https://universe.leagueoflegends.com/fr_FR/story/champion/{champion_name_clean}"

            driver.get(url)
            time.sleep(3)  # Attendre que la page se charge

            div = driver.find_element(By.ID, "CatchElement")
            contenu_div = div.get_attribute('innerHTML')
            soup = BeautifulSoup(contenu_div, 'html.parser')
            texte_propre = soup.get_text()
            personnage = champion_name_clean

            new_entry = {"personnage": personnage, "biographie": texte_propre}

            # Tente de lire les données existantes dans bio.json
            if os.path.exists("bio.json"):
                with open("bio.json", "r", encoding="utf-8") as json_file:
                    try:
                        data = json.load(json_file)
                    except json.JSONDecodeError:
                        data = []
            else:
                data = []

            data.append(new_entry)

            # Écrire les données accumulées dans le fichier JSON
            with open("bio.json", "w", encoding="utf-8") as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)

        driver.quit()

        return render_template('index.html', html_content="Toutes les biographies ont été récupérées avec succès.")

    except Exception as e:
        return render_template('index.html', html_content=f"Une erreur est survenue : {str(e)}")

@app.route('/download')
def download_file():
    if os.path.exists("bio.json"):
        return send_file("bio.json", as_attachment=True)
    return "Fichier non trouvé", 404

if __name__ == '__main__':
    app.run(debug=True)
