[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&size=50&pause=1000&center=true&vCenter=true&width=800&height=89&lines=6scrapper+by+AMINE)](https://git.io/typing-svg)

# League of Legends Champion Biography Scraper

Cette application permet de récupérer les biographies des champions de League of Legends à partir du site officiel et de les enregistrer dans un fichier JSON. L'application utilise Flask pour le backend et Selenium pour l'automatisation du navigateur afin de récupérer les données des pages web.

## Prérequis

Avant de commencer, assurez-vous d'avoir installé les éléments suivants sur votre machine :

- **Python 3.x**
- **pip** (le gestionnaire de paquets pour Python)
- **Google Chrome** (installé sur votre système)
- Les bibliothèques Python nécessaires :
  - `Flask`
  - `selenium`
  - `webdriver_manager`
  - `beautifulsoup4`
  - `lxml` (ou un autre parser HTML compatible)

### Installation des dépendances

Pour installer les dépendances nécessaires, exécutez la commande suivante dans votre terminal :

```bash
pip install flask selenium webdriver_manager beautifulsoup4 lxml
```

## Fichiers inclus

- `app.py` : le script principal de l'application Flask.
- `champions.json` : un fichier contenant la liste de tous les champions de League of Legends (vous devez fournir ce fichier).
- `bio.json` : le fichier de sortie qui contiendra les biographies des champions (généré automatiquement).
- `templates/index.html` : le fichier HTML pour l'interface utilisateur.

## Structure du projet

```
/project-directory
│
├── app.py
├── champions.json
├── bio.json (généré après exécution)
├── templates
│   └── index.html
└── README.md
```

## Comment utiliser l'application

### Étape 1 : Cloner le projet

Clonez ce dépôt GitHub sur votre machine locale :

```bash
git clone https://github.com/ABBESAmine/6scrapper
cd 6scrapper
```


### Étape 2 : Lancer l'application

Dans le répertoire du projet, exécutez la commande suivante pour démarrer l'application Flask :

```bash
python app.py
```

L'application sera accessible à l'adresse suivante : [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

### Étape 3 : Utilisation de l'application

- **Page d'accueil** : Entrez le nom d'un champion dans le champ de texte et cliquez sur "Récupérer la biographie". Cela récupérera la biographie du champion et l'enregistrera dans `bio.json`.

- **Launch** : Cliquez sur le bouton "Launch" pour récupérer les biographies de **tous** les champions listés dans `champions.json`. Ce processus peut prendre quelques minutes en fonction du nombre de champions.

- **Téléchargement du fichier JSON** : Une fois les biographies récupérées, vous pouvez télécharger le fichier `bio.json` en cliquant sur le bouton de téléchargement.

### Étape 4 : Télécharger les biographies

Lorsque les biographies sont récupérées avec succès, vous pouvez les télécharger en visitant cette URL : [http://127.0.0.1:5000/download](http://127.0.0.1:5000/download) ou en appuyant sur le bouton download.

## Configuration avancée

### Modification du comportement du navigateur

L'application utilise Selenium avec le mode **headless** de Google Chrome (sans interface graphique). Si vous souhaitez observer le processus de scraping en direct, vous pouvez retirer l'argument `--headless` dans la fonction `init_driver()` dans le fichier `app.py` :

```python
options.add_argument("--headless")  # Retirer cette ligne pour afficher la fenêtre du navigateur
```

### Gestion des erreurs

Si l'application ne parvient pas à récupérer la biographie d'un champion, un message d'erreur sera affiché dans le fichier JSON et dans l'interface utilisateur.

## Déploiement

### Hébergement sur GitHub Pages

GitHub Pages ne prend pas en charge l'hébergement d'applications back-end comme Flask. Vous devrez donc déployer votre application sur une plateforme comme **Heroku**, **Render**, ou **Railway.app** si vous souhaitez l'héberger en ligne.

## Problèmes connus

- Le scraping des pages peut prendre un certain temps en fonction de la vitesse de la connexion internet et de la réactivité du site web source.
- Si une page de champion change de structure (par exemple, si le site officiel de League of Legends modifie la manière dont les biographies sont affichées), l'application peut ne plus fonctionner correctement. Dans ce cas, il faudra ajuster le code du scraper pour s'adapter aux nouvelles structures HTML.

## Contributions

Les contributions à ce projet sont les bienvenues. Si vous trouvez un bug ou souhaitez ajouter de nouvelles fonctionnalités, n'hésitez pas à ouvrir une issue ou à soumettre une pull request.
