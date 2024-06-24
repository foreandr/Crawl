import requests
from bs4 import BeautifulSoup
import lxml
import re
import functions
import time

initial_link = 'https://rumble.com/'
driver = functions.open_site_selenium(initial_link)

crawl_object = {
    "urls_crawled":[],
    "urls_to_crawl":[],
    "urls_stored":[],
    "urls_to_store":[],
} 

def is_channel_template(url):
    pattern = r'\/c\/[A-Za-z0-9]+$'
    return bool(re.search(pattern, url))

def is_video_template(url):
    pattern = r'\/v[0-9a-z]{4,10}-[a-z0-9-.]+(?:\.html)?$'
    return bool(re.search(pattern, url))

def get_all_urls(soup):
    urls = []
    for link in soup.find_all('a'):
        try:
            href = link.get('href')
            if "http" in href:
                urls.append(href)
            else:
                urls.append(f"https://rumble.com{href}")
        except Exception as e:
            # print("ERROR CRAWLING", e, href)
            continue

    return urls

def parition_rumble_links(urls):
    channels = []
    posts = []
    for url in urls:
        if url == None:
            continue
        try:
            if is_channel_template(url):
                channels.append(url)

            if is_video_template(url):
                posts.append(url)
        except Exception as e:
            # print("ERROR CRAWLING", e, url)
            continue
    
    return list(set(channels)), list(set(posts))

def init_crawl_rumble():
    global driver
    soup = functions.get_driver_soup(driver)
    urls = get_all_urls(soup)
    channels, posts = parition_rumble_links(urls)
    recursive_crawler(posts, channels)

def recursive_crawler(posts, channels):
    all_urls = []
    total_posts = len(posts)

    # Process posts
    start_time_posts = time.time()
    for i, url in enumerate(posts, 1):
        driver.get(url)
        soup = functions.get_driver_soup(driver)
        urls = get_all_urls(soup)
        all_urls.extend(urls)

        # Print progress for posts
        elapsed_time_posts = time.time() - start_time_posts
        progress_posts = (i / total_posts) * 100
        print(f"[{i} / {total_posts}] - Posts Progress: {progress_posts:.2f}%, Elapsed time: {elapsed_time_posts:.2f} seconds")
    
    # Process channels
    start_time_channels = time.time()
    total_channels = len(channels)
    for i, url in enumerate(channels, 1):
        driver.get(url)
        soup = functions.get_driver_soup(driver)
        urls = get_all_urls(soup)
        all_urls.extend(urls)

        # Print progress for channels
        elapsed_time_channels = time.time() - start_time_channels
        progress_channels = (i / total_channels) * 100
        print(f"[{i} / {total_channels}] Channels Progress: {progress_channels:.2f}%, Elapsed time: {elapsed_time_channels:.2f} seconds")
    
    channels_, posts_ = parition_rumble_links(all_urls)
    new_urls_combined = posts_ + channels_
    param_urls_combined = posts + channels
    unique_urls = [url for url in new_urls_combined if url not in param_urls_combined]

    print("new_urls_combined", len(new_urls_combined))
    print("param_urls_combined", len(param_urls_combined))
    print("unique_urls", len(unique_urls))
    
    new_channels_to_scrape, new_posts_to_scrape = parition_rumble_links(unique_urls)
    print("new_channels_to_scrape", len(new_channels_to_scrape))
    print("new_posts_to_scrape", len(new_posts_to_scrape))
 
    recursive_crawler(new_posts_to_scrape, new_channels_to_scrape)

if __name__ == "__main__":
    init_crawl_rumble()

    driver.close()