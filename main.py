import functions
from urllib.parse import urlparse
import re
import time
from hyperSel import hyperSel
import link_detection
import db

initial_link = 'https://snse.ca'
driver = hyperSel.open_site_selenium(initial_link)

def get_seed_links():
    return ["https://www.youtube.com/watch?v=MK4DY9ld77k", "https://www.rumble.com",'https://odysee.com/',]

def get_website_name(url):
    # Use regex to extract main domain name
    domain = re.search(r"(?:https?://)?(?:www\d{0,3}\.)?([a-zA-Z0-9.-]+)\.", url).group(1)
    return domain

def partition_data(urls):
    content = []
    channels = []

    for url in urls:
        url_type = link_detection.identify_video_platform(url)
        if url_type == "content":
            content.append(url)
        if url_type == "channel":
            channels.append(url)
        
    return content, channels

def crawler(all_urls):
    #TODO: i want this to be multithreaded
    #TODO detect whether use soup ro driver based on site
    new_urls = []

    total = len(all_urls)
    fifth_percentage = max(int((5 / 100) * len(all_urls)), 1)
    start_time_posts = time.time()
    start = time.time()
    
    for i, url in enumerate(all_urls, 1):
        if not db.can_scrape(url):
            print("SCRAPED TOO RECENTLY", url)
            continue
        site_type = get_website_name(url)

        try:
            driver.get(url)
        except Exception as e:
            print("FAILED TO GET URL SKIPPING", e)
            continue
        time.sleep(0.5)

        # GET CONTENT
        soup = hyperSel.get_driver_soup(driver)
        urls = functions.get_all_typed_urls(soup, site_type)

        new_content, new_channels = partition_data(urls)

        # INSERT CONTENT
        # insert_urls_into_db(new_content)
        # insert_channels_into_db(new_channels)

        for j in new_content + new_channels:
            if j not in new_urls:
                new_urls.append(j)

        if i % fifth_percentage == 0:
            elapsed_time_posts = time.time() - start_time_posts
            progress_posts = (i / total) * 100
            loc_prog = time.time() - start
            print(f"[{i} / {total}][:{progress_posts:.2f}%][TOT:{elapsed_time_posts:.2f}][LOC:{loc_prog:.2f}][all_urls: {len(all_urls)}]")
            start = time.time()

    current_urls = functions.get_all_urls()
    for url in new_urls:
        if url not in current_urls:
            functions.add_url(url)

    crawler(new_urls)

def main():
    seed_links = get_seed_links()
    crawler(all_urls=seed_links)

if __name__ == "__main__":
    main()