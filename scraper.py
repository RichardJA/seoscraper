import page

# This code isn't needed unless I decide to use Selenium
# chromedriver = "C:\\Users\\Richard\\Documents\\Programs\\chromedriver.exe"

domain = "http://www.tearfund.org"
start_url = 'http://www.tearfund.org/'

pages = []
pages_status = {}


def get_full_url(url):
    """
    Takes the page text passed through and finds all the links
    Checks whether the link is an internal link and if not ignores it
    If not already part of dictionary, adds it and sets default value to 0
    Value should only ever be set to 1 if the page is scraped
    """
    if url[0] == "/":
        url = domain + url
    elif url[0:4] != "http":
        url = domain + url
    if not any(url in d for d in pages_status):
        pages_status.append({url, 0})
    print(pages_status)
    return url


def check_page_level():
    # not sure how to do this one yet - but need to store the minimum number of clicks to get to page
    pass


def store_results(the_results):
    # store the results in a google sheet
    pass


def main():
    print('Starting Scrape...')
    print('Setting homepage to ' + start_url)
    pages_status.setdefault(start_url, 0)
    pages.append(page.Page(start_url))
    pages_status[start_url] = 1
    print("Homepage processed")
    print("Title Value:", pages[0].title_text, "\nTitle Length:", pages[0].title_length, "\nAll Links:", pages[0].all_links)
    current_url = ""
    while True:
        for k, v in pages_status.items():
            if v == 0:
                current_url = k
                print(current_url)

        pages_status.setdefault(current_url, 0)

        #pages.append(page.Page(current_url))
        if 0 in pages_status.values():
            print("All Pages Completed")
            break




if __name__ == '__main__':
    main()
