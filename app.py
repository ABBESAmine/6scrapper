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
app.secret_key = os.urandom(12)

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        champion_name = request.form['name'].strip().lower().replace(" ", "")
        url = "https://universe.leagueoflegends.com/fr_FR/story/champion/" + champion_name
        
        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver.get(url)

            time.sleep(3)

            try:
                div = driver.find_element(By.ID, "CatchElement")
                contenu_div = div.get_attribute('innerHTML')

                soup = BeautifulSoup(contenu_div, 'html.parser')
                texte_propre = soup.get_text()

                personnage = url.split('/')[-1]

                new_entry = {
                    "personnage": personnage,
                    "biographie": texte_propre
                }

                if os.path.exists("bio.json"):
                    with open("bio.json", "r", encoding="utf-8") as json_file:
                        try:
                            data = json.load(json_file)  
                        except json.JSONDecodeError:
                            data = []
                else:
                    data = []

                if not isinstance(data, list):
                    data = [] 

                data.append(new_entry)

                with open("bio.json", "w", encoding="utf-8") as json_file:
                    json.dump(data, json_file, ensure_ascii=False, indent=4)
                
                flash('Chargement de données effectué. Téléchargement disponible')

            except Exception as e:
                flash(f"Erreur lors de la récupération de la div : {str(e)}")

            driver.quit()

        except Exception as e:
            flash(f"Une erreur est survenue : {str(e)}")
        
        return redirect('/')

    return render_template('index.html', html_content=None)

@app.route('/download')
def download_file():
    if os.path.exists("bio.json"):
        return send_file("bio.json", as_attachment=True)
    return "Fichier non trouvé", 404

if __name__ == '__main__':
    app.run(debug=True)
