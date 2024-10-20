from flask import Flask, render_template, request, jsonify, send_file, Response
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
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
#options.add_argument("--window-size=1920x1080")

# Fonction pour initialiser le driver
def init_driver():
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Fonction commune pour scraper et stocker la biographie
def scrape_and_store_biography(champion_name, driver):
    try:
        # Nettoyage du nom du champion pour correspondre à l'URL
        champion_name_clean = champion_name.strip().lower().replace(" ", "").replace("'", "").replace(".", "").replace("é", "e").replace("î", "i")
        url = f"https://universe.leagueoflegends.com/fr_FR/story/champion/{champion_name_clean}"

        driver.get(url)
        time.sleep(3)  # Attendre que la page se charge

        div = driver.find_element(By.ID, "CatchElement")
        contenu_div = div.get_attribute('innerHTML')
        soup = BeautifulSoup(contenu_div, 'html.parser')
        texte_propre = soup.get_text()

        new_entry = {"personnage": champion_name_clean, "biographie": texte_propre}

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

        return champion_name_clean

    except Exception as e:
        print(f"Erreur lors du scraping du champion {champion_name}: {str(e)}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    driver = init_driver()
    if request.method == 'POST':
        champion = request.form['name']
        scrape_and_store_biography(champion, driver)

    return render_template('index.html')

# Route SSE pour envoyer la progression du scraping
@app.route('/progress')
def progress():
    def generate():
        driver = init_driver()

        if not os.path.exists("champions.json"):
            yield "data: Le fichier champions.json est introuvable\n\n"
            return

        with open("champions.json", "r") as file:
            champions = json.load(file)

        if not champions:
            yield "data: La liste des champions est vide\n\n"
            return

        for champion_name in champions:
            scraped_champion = scrape_and_store_biography(champion_name, driver)
            if scraped_champion:
                yield f"data: {scraped_champion}\n\n"
            else:
                yield f"data: Erreur lors du scraping de {champion_name}\n\n"

        driver.quit()

    return Response(generate(), mimetype='text/event-stream')

# Route pour afficher les champions récupérés
@app.route('/get_scraped_champions')
def get_scraped_champions():
    if os.path.exists("bio.json"):
        with open("bio.json", "r", encoding="utf-8") as json_file:
            try:
                data = json.load(json_file)
                champions = [entry["personnage"] for entry in data]
                return jsonify(champions)
            except json.JSONDecodeError:
                return jsonify([])
    return jsonify([])

# Route pour télécharger le fichier bio.json
@app.route('/download')
def download_file():
    if os.path.exists("bio.json"):
        return send_file("bio.json", as_attachment=True)
    return "Fichier non trouvé", 404


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Utilise le port fourni par Render, ou 5000 par défaut
    app.run(host='0.0.0.0', port=port)