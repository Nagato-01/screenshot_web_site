
# Bulk Screenshot Capture

Ce projet permet de :
- Récupérer les URLs des sites à capturer.
- Prendre des captures d'écran de chaque site.
- Récupérer le code HTML et les ressources associées (CSS, images, vidéos).

## Arborescence du projet

```plaintext
bulk-screenshot-capture/
├── bulk_screenshot_capture.py  # Script pour les captures d'écran en masse
├── capture_urls.csv            # Fichier contenant les URLs à capturer
├── env/                        # Environnement virtuel Python
├── .gitignore                  # Fichier pour ignorer certains fichiers dans Git
├── README.md                   # Ce fichier
├── save_url.py                 # Script pour récupérer et sauvegarder les URLs
├── scraped_pages/              # Dossier contenant les pages HTML récupérées
├── scrap_html.py               # Script pour récupérer le code HTML et les ressources
├── screenshots/                # Dossier contenant les captures d'écran
```

---

## Pré-requis

1. **Python installé :**
   - Assurez-vous d'avoir Python 3.10 ou une version supérieure installée.

2. **Chromedriver installé :**
   - Téléchargez et installez [Chromedriver](https://chromedriver.chromium.org/) correspondant à la version de votre navigateur Google Chrome.

3. **Git installé :**
   - Assurez-vous d'avoir installé Git pour cloner et gérer le projet.

---

## Configuration de l'environnement virtuel

1. **Créer un environnement virtuel :**
   ```bash
   python3 -m venv env
   ```

2. **Activer l'environnement virtuel :**
   - Sur Linux/Mac :
     ```bash
     source env/bin/activate
     ```
   - Sur Windows :
     ```cmd
     .\env\Scripts\activate
     ```

3. **Installer les dépendances requises :**
   ```bash
   pip install -r requirements.txt
   ```

---

## Lancer les différents scripts

### 1. Récupérer les URLs des sites

Le script `save_url.py` permet de récupérer et de sauvegarder les URLs dans le fichier `capture_urls.csv`.

```bash
python save_url.py
```

Assurez-vous que le fichier `capture_urls.csv` contient une URL valide par ligne.

---

### 2. Lancer les captures d'écran

Le script `bulk_screenshot_capture.py` capture des captures d'écran normales et pleine page des sites listés dans `capture_urls.csv`.

```bash
python bulk_screenshot_capture.py
```

Les captures seront enregistrées dans le dossier `screenshots/`, suivant une arborescence organisée par type (normal, full screen) et par appareil (desktop, tablet, mobile).

---

### 3. Récupérer le code HTML et les ressources associées

Le script `scrap_html.py` permet de récupérer le code HTML des sites ainsi que les ressources associées (CSS, images, vidéos).

```bash
python scrap_html.py
```

Les pages récupérées et leurs ressources seront enregistrées dans le dossier `scraped_pages/`.

---

## Contribuer

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/Nagato-01/screenshot_web_site.git
   cd bulk-screenshot-capture
   ```

2. Créez une branche pour vos modifications :
   ```bash
   git checkout -b feature/nom-de-la-feature
   ```

3. Ajoutez vos modifications :
   ```bash
   git add .
   git commit -m "Ajout d'une nouvelle fonctionnalité"
   git push origin feature/nom-de-la-feature
   ```

4. Ouvrez une Pull Request sur GitHub.

---

## Auteurs

- **Nagato-01** - Créateur et mainteneur du projet.

---

## Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.
