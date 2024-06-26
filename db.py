def connect_to_db():
    return None

CONN = connect_to_db()

def insert_urls_into_db(urls):
    global CONN
    # default set scrapetime to null
    # on conflict DO NOTHING
    pass

def insert_channels_into_db(urls):
    global CONN
    # default set scrapetime to null
    # on conflict DO NOTHING
    pass

def can_scrape(url):
    global CONN
    # 1. GET MOST RECENT SCRAPETIME IF EXISTS
    # 2. IF SCRAPETIME LONGER THAN THRESHOLD, SCRAPE, AND SET TO NOW()
    # 3. ELSE CONTINUE
    return True