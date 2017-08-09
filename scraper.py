import page

# This code isn't needed unless I decide to use Selenium
# chromedriver = "C:\\Users\\Richard\\Documents\\Programs\\chromedriver.exe"

domain = "http://www.tearfund.org"
start_url = 'http://www.tearfund.org/'

pages = []
pages_status = []


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

    pages.append(page.Page(start_url))
    pages_status.append({start_url, 0})
    for n in pages_status:
        if start_url in n:
            print("in")

if __name__ == '__main__':
    main()
