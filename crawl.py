import functions
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
    pass

def insert_channels_into_db(urls):
    pass

def crawler(content, channels):
    all_urls = content + channels

    for url in all_urls:
        # grab most recent scrapetime of url
        # if url doesnt exist, or scraped a while back, good
        # else continue

        soup = get_soup(url)
        urls = get_urls(soup)
        new_content, new_channels  = partition_data(urls)

        insert_urls_into_db(content) # on conflict update scrapteimte to now
        insert_channels_into_db(channels) # on conflict update scrapteimte to now

        crawler(new_content, new_channels)