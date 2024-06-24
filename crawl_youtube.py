import functions
if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=GO0DuQWgwII"
    soup = functions.get_soup(url)
    functions.test_log(soup)
    print(soup)
    urls = functions.get_all_urls(soup)
    # print("urls", urls)
