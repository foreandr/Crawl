import requests
from bs4 import BeautifulSoup
import lxml
import re
import functions
import time

initial_link = 'https://rumble.com/'
driver = functions.open_site_selenium(initial_link)

def is_channel_template(url):
    pattern = r'\/c\/[A-Za-z0-9]+$'
    return bool(re.search(pattern, url))

def is_video_template(url):
    pattern = r'\/v[0-9a-z]{4,10}-[a-z0-9-.]+(?:\.html)?$'
    return bool(re.search(pattern, url))

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
    urls = functions.get_all_rumble_urls(soup)
    if len(urls) == 0:
        init_crawl_rumble()

    channels, posts = parition_rumble_links(urls)
    recursive_crawler(posts, channels)


def recursive_crawler(posts, channels):
    all_urls = []
    total_posts = len(posts)
    total_channels = len(channels)

    all_urls.extend(functions.get_urls_from_list_of_urls(driver, posts, total_posts))
    all_urls.extend(functions.get_urls_from_list_of_urls(driver, channels, total_channels))
    print("all_urls", len(all_urls))

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
