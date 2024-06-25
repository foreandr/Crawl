import functions
import time
initial_link = 'https://www.youtube.com/watch?v=GO0DuQWgwII'
driver = functions.open_site_selenium(initial_link)
import re

def is_video_template(url):
    # Pattern to match YouTube video URLs
    video_pattern = r'^https?://(?:www\.)?youtube\.com/watch\?v=[A-Za-z0-9_-]+$'
    return bool(re.search(video_pattern, url))

def is_channel_template(url):
    # Pattern to match YouTube channel URLs including @ sign
    channel_pattern = r'^https?://(?:www\.)?youtube\.com/(?:c(?:hannel)?/|@)?[A-Za-z0-9_-]+(?:/|$)'
    return bool(re.search(channel_pattern, url))
def main():# 1
    time.sleep(3)
    soup = functions.get_driver_soup(driver)
    urls = functions.get_all_youtube_urls(soup)

    channels = []
    videos = []
    for url in urls:

        if is_video_template(url):
            if url in videos:
                continue
            videos.append(url)
            continue

        if is_channel_template(url):
            cleaned_url = url.replace("/about", "").replace("/videos", "")
            if cleaned_url in channels:
                continue
            channels.append(cleaned_url)
            continue

    for channel in channels:
        print("channel",channel)

    for video in videos:
        print("video", video)

if __name__ == "__main__":
    main()

