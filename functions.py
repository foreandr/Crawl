#test
import requests
from bs4 import BeautifulSoup
import random
import time

def test_log(text_to_write, append_or_wipe='a'):
    file_path = './test.txt'
    with open(file_path, append_or_wipe, encoding='utf-8') as file:
        file.write(f"{str(text_to_write)}\n")

def add_url(url):
    file_path = './urls.txt'
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(f"{str(url)}\n")

def get_all_urls():
    file_path = './urls.txt'
    urls = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            urls.append(line.strip())
    return urls

def get_soup(url):
    # List of common user agents
    user_agents = [
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    ]

    # Headers
    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

def get_all_hrefs(soup):
    hrefs = []
    for link in soup.find_all('a'):
        try:
            href = link.get('href')
            hrefs.append(href)
        except Exception as e:
            # print("ERROR CRAWLING", e, href)
            continue

    return hrefs

def get_all_typed_urls(soup, site_type):
    hrefs = get_all_hrefs(soup)
    urls = []
    for href in hrefs:
        urls.append(f"https://{site_type}.com{href}")

    return urls

