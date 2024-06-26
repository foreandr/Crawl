import functions
from urllib.parse import urlparse
import re
import time
import hyperSel

initial_link = 'https://snse.ca'
driver = functions.open_site_selenium(initial_link)
def get_seed_links():
    return ["https://www.youtube.com/watch?v=MK4DY9ld77k", "https://www.rumble.com",'https://odysee.com/',]
def get_website_name(url):
    # Use regex to extract main domain name
    domain = re.search(r"(?:https?://)?(?:www\d{0,3}\.)?([a-zA-Z0-9.-]+)\.", url).group(1)
    return domain

def get_soup(url):
    # DRIVER IF NEEDED
    urls = functions.get_soup(url)
    pass
def get_urls(soup):

    pass

def preprocess(urls):
    urls = set(list(clean_urls(urls)))
    return urls

def clean_urls(urls):
    "youtube"
    "rumble"
    "etc.."
    return []
def partition_data(urls):
    content = []
    channels = []
    return content, channels

def insert_urls_into_db(urls):
    # default set scrapetime to null
    # on conflict DO NOTHING
    pass

def insert_channels_into_db(urls):
    # default set scrapetime to null
    # on conflict DO NOTHING
    pass

def can_scrape(url):
    # 1. GET MOST RECENT SCRAPETIME IF EXISTS
    # 2. IF SCRAPETIME LONGER THAN THRESHOLD, SCRAPE, AND SET TO NOW()
    # 3. ELSE CONTINUE
    return True

def crawler(all_urls):
    new_urls = []

    total = len(all_urls)
    fifth_percentage = max(int((5 / 100) * len(all_urls)), 1)
    start_time_posts = time.time()
    start = time.time()

    for i, url in enumerate(all_urls, 1):
        site_type = get_website_name(url)
        print("SCRAPING URL", url)
        if not can_scrape(url):
            print("SCRAPED TOO RECENTLY", url)
            continue

        driver.get(url)
        time.sleep(2)

        # GET CONTENT
        soup = functions.get_driver_soup(driver)
        urls = functions.get_all_typed_urls(soup, site_type)

        new_content, new_channels = partition_data(urls)
        print("new_content", new_content)
        print("new_channels",new_channels)

        # INSERT CONTENT
        insert_urls_into_db(new_content)
        insert_channels_into_db(new_channels)

        for j in new_content + new_channels:
            new_urls.append(j)

        if i % fifth_percentage == 0:
            elapsed_time_posts = time.time() - start_time_posts
            progress_posts = (i / total) * 100
            loc_prog = time.time() - start
            print(f"[{i} / {total}][:{progress_posts:.2f}%][TOT:{elapsed_time_posts:.2f}][LOC:{loc_prog:.2f}][all_urls: {len(all_urls)}]")
            start = time.time()

    print('new urls')
    for j in new_urls:
        print(j)
    exit()
    crawler(new_urls)

def main():
    seed_links = get_seed_links()
    crawler(all_urls=seed_links)

if __name__ == "__main__":
    main()