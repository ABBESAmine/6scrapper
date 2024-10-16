import requests
import json  # Importation de la bibliothèque json

# URL de l'API pour récupérer les informations sur les champions
url = "https://ddragon.leagueoflegends.com/cdn/14.20.1/data/fr_FR/champion.json"

# Faire une requête pour obtenir les données
response = requests.get(url)

# Vérifier si la requête a réussi
if response.status_code == 200:
    data = response.json()
    
    # Récupérer le nom de tous les champions
    champion_names = [champion['name'] for champion in data['data'].values()]

    # Enregistrer les noms des champions dans un fichier JSON
    with open('champions.json', 'w', encoding='utf-8') as json_file:
        json.dump(champion_names, json_file, ensure_ascii=False, indent=4)

    print("Les noms des champions ont été enregistrés dans champions.json.")
else:
    print(f"Erreur lors de la récupération des données : {response.status_code}")
