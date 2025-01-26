from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from urllib.parse import urlparse
import os
import csv
import requests
from bs4 import BeautifulSoup
import logging
import shutil

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

def save_file(content, file_path):
    """Enregistre un fichier localement."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'wb') as file:
        file.write(content)
    logging.info(f"Fichier sauvegardé : {file_path}")

def download_resources(base_url, soup, output_dir):
    """Télécharge les ressources (images, vidéos, CSS) depuis une page HTML."""
    resources = {
        "img": "src",
        "video": "src",
        "link": "href"  # Principalement pour les fichiers CSS
    }

    for tag, attr in resources.items():
        for element in soup.find_all(tag):
            resource_url = element.get(attr)
            if not resource_url:
                continue
            if resource_url.startswith("//"):
                resource_url = "https:" + resource_url
            elif resource_url.startswith("/"):
                resource_url = base_url.rstrip("/") + resource_url
            try:
                response = requests.get(resource_url, stream=True)
                if response.status_code == 200:
                    file_name = os.path.basename(resource_url.split("?")[0])
                    file_path = os.path.join(output_dir, tag, file_name)
                    save_file(response.content, file_path)
            except Exception as e:
                logging.error(f"Erreur lors du téléchargement de {resource_url} : {e}")

def scrape_page(url, output_dir):
    """Récupère le code HTML, CSS, et les ressources d'une page."""
    driver = setup_driver()
    try:
        driver.get(url)
        driver.implicitly_wait(10)
        html_content = driver.page_source
        save_file(html_content.encode('utf-8'), os.path.join(output_dir, "page.html"))
        soup = BeautifulSoup(html_content, "html.parser")
        download_resources(url, soup, output_dir)
    finally:
        driver.quit()

def validate_and_format_url(url):
    """Valide et formate l'URL pour s'assurer qu'elle est correcte."""
    if not url:
        return None
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        url = "https://" + url
        parsed_url = urlparse(url)
    if not parsed_url.netloc:
        return None
    try:
        response = requests.head(url, timeout=5)
        if response.status_code >= 400:
            logging.warning(f"URL inaccessible : {url} (Code HTTP {response.status_code})")
            return None
    except requests.RequestException as e:
        logging.warning(f"Erreur lors de l'accès à l'URL : {url} ({e})")
        return None
    return url

def main():
    output_dir_base = "./scraped_pages"
    os.makedirs(output_dir_base, exist_ok=True)
    csv_file_path = './capture_urls.csv'
    if not os.path.exists(csv_file_path):
        logging.error(f"Le fichier {csv_file_path} n'existe pas.")
        return
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        url_reader = csv.reader(csvfile, delimiter=',')
        for row in url_reader:
            if not row or len(row) < 1:
                continue
            raw_url = row[0].strip()
            try:
                url = validate_and_format_url(raw_url)
                if url:
                    logging.info(f"Traitement de l'URL : {url}")
                    url_output_dir = os.path.join(output_dir_base, clean_url(url))
                    scrape_page(url, url_output_dir)
                else:
                    logging.warning(f"URL invalide ignorée : {raw_url}")
            except Exception as e:
                logging.error(f"Erreur lors du traitement de l'URL {raw_url} : {e}")
                # Continuer avec l'URL suivante

def clean_url(url):
    return url.replace("http://", "").replace("https://", "").replace("/", "_").replace("?", "_").replace("&", "_")[:100]

if __name__ == "__main__":
    main()
