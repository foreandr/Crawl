#test
import requests
from bs4 import BeautifulSoup
import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

urls_crawled = []


def test_log(text_to_write, append_or_wipe):
    file_path = './test.txt'
    with open(file_path, append_or_wipe, encoding='utf-8') as file:
        file.write(f"{str(text_to_write)}\n")


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


def get_driver_soup(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, features="lxml")
    return soup


def open_site_selenium(site, show_browser=False):
    options = Options()
    if not show_browser:
        options.add_argument("--headless")  # Run in headless mode

    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36")
    options.add_argument("--start-maximized")
    options.add_argument("--log-level=3")
    options.add_argument("-log-level=OFF")
    options.add_argument("--disable-logging")  # Disable logging
    options.add_argument("--start-minimized")  # Start minimized

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(site)
    return driver


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

def get_all_rumble_urls(soup):
    hrefs = get_all_hrefs(soup)
    urls = []
    for href in hrefs:
        urls.append(f"https://rumble.com{href}")

    return urls

def get_all_youtube_urls(soup):
    hrefs = get_all_hrefs(soup)
    urls = []
    for href in hrefs:
        urls.append(f"https://youtube.com{href}")

    return urls

def get_urls_from_list_of_urls(driver, posts, total):
    start_time_posts = time.time()
    start = time.time()
    all_urls = []
    fifth_percentage = max(int((5 / 100) * total), 1)

    for i, url in enumerate(posts, 1):

        if url in urls_crawled:
            print("skipping", url)
            continue

        urls_crawled.append(url)
        driver.get(url)
        soup = get_driver_soup(driver)
        urls = get_all_urls(soup)
        all_urls.extend(urls)

        # Print progress for posts
        if i % fifth_percentage == 0:
            elapsed_time_posts = time.time() - start_time_posts
            progress_posts = (i / total) * 100
            loc_prog = time.time() - start
            print(f"[{i} / {total}][:{progress_posts:.2f}%][TOT:{elapsed_time_posts:.2f}][LOC:{loc_prog:.2f}][all_urls: {len(all_urls)}]")
            start = time.time()

    return list(set(all_urls))
