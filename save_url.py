from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import os
import csv
import time
import logging
import shutil

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Formats d'affichage
VIEWPORTS = {
    "desktop": {"width": 1920, "height": 1080},
    "tablet": {"width": 768, "height": 1024},
    "mobile": {"width": 375, "height": 812},
}

def clean_url(url):
    """Nettoie l'URL pour l'utiliser comme nom de fichier."""
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url.replace('/', '_').replace(':', '_').replace('?', '_').replace('&', '_')[:100]

def setup_driver():
    """Configure et retourne le driver Selenium."""
    chromedriver_path = shutil.which("chromedriver")
    if not chromedriver_path:
        raise FileNotFoundError("Chromedriver n'est pas installé ou non accessible.")
    
    service = Service(executable_path=chromedriver_path)
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-cookies")
    return webdriver.Chrome(service=service, options=options)

def create_directory_structure(base_folder):
    """Crée la structure des dossiers nécessaires."""
    sub_folders = ["normal", "full_screen"]
    for sub in sub_folders:
        for format_name in VIEWPORTS.keys():
            os.makedirs(os.path.join(base_folder, sub, format_name), exist_ok=True)

def wait_for_page_to_load(driver, timeout=30):
    """Attendre que la page soit complètement chargée."""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
    except Exception as e:
        logging.warning(f"La page a mis trop de temps à se charger : {e}")

def capture_screenshot(driver, url, output_path, viewport):
    """Capture une capture d'écran normale pour un format donné."""
    try:
        driver.set_window_size(viewport["width"], viewport["height"])
        driver.get(url)
        wait_for_page_to_load(driver)  # Assurez-vous que la page est chargée
        driver.save_screenshot(output_path)
        logging.info(f"Capture normale enregistrée : {output_path}")
    except Exception as e:
        logging.error(f"Erreur lors de la capture normale pour {url}: {e}")

def capture_full_page_screenshot(driver, url, output_path):
    """Capture une capture d'écran pleine page."""
    try:
        driver.get(url)
        wait_for_page_to_load(driver)  # Assurez-vous que la page est chargée
        total_height = driver.execute_script("return document.body.scrollHeight")
        viewport_width = driver.execute_script("return window.innerWidth")
        driver.set_window_size(viewport_width, total_height)
        driver.save_screenshot(output_path)
        logging.info(f"Capture pleine page enregistrée : {output_path}")
    except Exception as e:
        logging.error(f"Erreur lors de la capture pleine page pour {url}: {e}")

def process_url(driver, url, base_folder):
    """Traite chaque URL et enregistre les captures dans les bons dossiers."""
    for format_name, viewport in VIEWPORTS.items():
        # Dossiers spécifiques pour chaque taille d'écran
        normal_output_dir = os.path.join(base_folder, "normal", format_name)
        full_output_dir = os.path.join(base_folder, "full_screen", format_name)
        
        # Fichiers de sortie
        normal_file_path = os.path.join(normal_output_dir, f"{clean_url(url)}.png")
        full_file_path = os.path.join(full_output_dir, f"{clean_url(url)}.png")
        
        # Capture normale
        try:
            capture_screenshot(driver, url, normal_file_path, viewport)
        except Exception as e:
            logging.error(f"Erreur lors de la capture normale pour {url} ({format_name}): {e}")
        
        # Capture pleine page
        try:
            capture_full_page_screenshot(driver, url, full_file_path)
        except Exception as e:
            logging.error(f"Erreur lors de la capture pleine page pour {url} ({format_name}): {e}")

def main():
    """Programme principal."""
    driver = setup_driver()
    base_folder = './screenshots'
    
    # Crée la structure des dossiers
    create_directory_structure(base_folder)

    try:
        with open('./capture_urls.csv', newline='') as csvfile:
            url_reader = csv.reader(csvfile, delimiter=',')
            for row in url_reader:
                url = row[0].strip()
                process_url(driver, url, base_folder)
    finally:
        driver.quit()
        logging.info("Traitement terminé pour toutes les URLs. 🏁")

if __name__ == "__main__":
    main()
