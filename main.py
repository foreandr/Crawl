import functions
import re
import time
from hyperSel import hyperSel
import link_detection
import db
import threading

initial_link = 'https://snse.ca'
driver = hyperSel.open_site_selenium(initial_link)

THREAD_COUNT = 0
RAM_THRESHOLD = 75

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

def get_urls_from_url(url):
    # GET CONTENT
    
    urls = []
    site_type = get_website_name(url)
    soup = hyperSel.get_driver_soup(driver)
    urls = functions.get_all_typed_urls(soup, site_type)
    new_content, new_channels = partition_data(urls) 
    
    new_content, new_channels = get_urls_from_url(url)
        
    # INSERT CONTENT
    # insert_urls_into_db(new_content)
    # insert_channels_into_db(new_channels)
        
    for j in new_content + new_channels:
        if j not in urls:
            urls.append(j)
    
    return new_content, new_channels

def crawler_loop(all_urls):
    new_urls = []
    total = len(all_urls)
    fifth_percentage = max(int((5 / 100) * len(all_urls)), 1)
    start_time_posts = time.time()
    start = time.time()
    
    for i, url in enumerate(all_urls, 1):
        functions.ram_checker(RAM_THRESHOLD)
        
        if not db.can_scrape(url):
            print("SCRAPED TOO RECENTLY", url)
            continue
        try:
            driver.get(url)
        except Exception as e:
            print("FAILED TO GET URL SKIPPING", e)
            continue
        
        new_urls.extend(get_urls_from_url(url))

        if i % fifth_percentage == 0:
            elapsed_time_posts = time.time() - start_time_posts
            progress_posts = (i / total) * 100
            loc_prog = time.time() - start
            print(f"[{i} / {total}][:{progress_posts:.2f}%][TOT:{elapsed_time_posts:.2f}][LOC:{loc_prog:.2f}][all_urls: {len(all_urls)}]")
            start = time.time()
            
    return new_urls
    
def crawler(all_urls):
    print(f"CRAWLING: [URLS:{len(all_urls)}][RAM:{functions.get_ram_percentage()}]")
    global THREAD_COUNT
    THREAD_COUNT+=1
    
    #TODO detect whether use soup ro driver based on site
    new_urls = crawler_loop(all_urls)
    current_urls = functions.get_all_urls()
    
    current_ram = functions.get_ram_percentage()
    for url in new_urls:
        if url not in current_urls:
            functions.add_url(url)
            
            if current_ram <= (RAM_THRESHOLD * .8):
                print(F"[RAM: {current_ram}][THREAD_COUNT:{THREAD_COUNT}] - BRANCHING", url)
                thread = threading.Thread(target=lambda: crawler([url]))
                thread.start()

    if current_ram >= (RAM_THRESHOLD * 1.1):
        print(f"RAM TOO HIGH, CLOSING THREAD. [THREAD_COUNT:{THREAD_COUNT}]")
        THREAD_COUNT-=1
        return 1
    
    return crawler(new_urls)

def main():
    seed_links = get_seed_links()
    crawler(all_urls=seed_links)

if __name__ == "__main__":
    main()