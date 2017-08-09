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
    elif url[0:3] == "www":
        url = "http://" + url
    elif url[0:4] != "http":
        url = domain + "/" + url
    print(url)
    return url


def check_page_level():
    # not sure how to do this one yet - but need to store the minimum number of clicks to get to page
    pass


def main():
    """
    Starts the program.
    Stores completed pages in a list and stores completed status within a dictionary
    """
    # The first iteration of this function is completed outside of the loop as the home page is hard coded.
    # After the first iteration, the variable changes to "current_url" and can then be looped
    print('Starting Scrape...')
    current_url = start_url
    pages_status.setdefault(current_url, 0)
    while True:
        pages_status[current_url] = 1
        temp_page = page.Page(current_url)
        pages.append(temp_page)

        for n in temp_page.all_links:
            current_url = get_full_url(n)
            pages_status.setdefault(current_url, 0)


        for k, v in pages_status.items():
            if v == 0:
                current_url = pages_status[k]
                print(current_url)
                break


        # for n in range(len(pages)):
        #     print(pages[n].page_url)
        #     #if pages_status[pages[n].page_url] == 0:
        #      #   pages_status[n] = 0
        # if 0 not in pages_status.values():
        #     print(pages_status.values())
        #     print("All Pages Completed")
        #     break
        # #
    # while True:
    #
    #     for k, v in pages_status.items():
    #         if v == 0 and current_url != k:

    #     pages_status.setdefault(current_url, 0)
    #     pages.append(page.Page(current_url))
    #     if 0 not in pages_status.values():
    #         print("All Pages Completed")
    #         break

if __name__ == '__main__':
    main()
