import re

def identify_video_platform(url):
    patterns = {
        # YOUTUBE
        "channel": r'^https?://(?:www\.)?youtube\.com/(?:c(?:hannel)?/|@)?[A-Za-z0-9_-]+(?:/|$)',
        "content": r'^https?://(?:www\.)?youtube\.com/watch\?v=[A-Za-z0-9_-]+$',
        
        # RUMBLE
        "channel": r'\/c\/[A-Za-z0-9]+$',
        "content": r'\/v[0-9a-z]{4,10}-[a-z0-9-.]+(?:\.html)?$'
    }
    
    for platform, pattern in patterns.items():
        if re.search(pattern, url):
            return platform
    
    return "Unknown"