# schemesapp/scraper.py

import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://data.gov.in"
HEADERS = {
    "User-Agent": "GovSchemesScraper/1.0 (contact@example.com)"
}

def scrape_schemes(page=0):
    url = f"https://data.gov.in/resources?filters%5Bfield_resource_type%5D=dataset&page={page}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to fetch page {page}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    schemes = []

    for resource in soup.find_all("div", class_="resource-item"):
        title_tag = resource.find("h3", class_="resource-title")
        if title_tag and title_tag.a:
            title = title_tag.a.text.strip()
            link = BASE_URL + title_tag.a['href']
            schemes.append({"title": title, "link": link})

    return schemes

def scrape_all_schemes(pages=2):
    all_schemes = []
    for page in range(pages):
        print(f"Scraping page {page}")
        schemes = scrape_schemes(page)
        all_schemes.extend(schemes)
        time.sleep(2)  # Be polite to the server
    return all_schemes
