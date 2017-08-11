import page
import requests
import storage

domain = "http://www.tearfund.org"
start_url = 'http://www.tearfund.org/'

# list and dictionary to store Page class items and url status
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
    return url


def add_to_dictionary(url):
    """
    Takes the url and checks to see whether it is a pdf or another file type
    These types of files will have issues being scanned so are cleaned out by this function
    """
    no_list = [".pdf", "pdf/", ".doc", "docx", ".ppt", "pptx"]
    if url[-4:] in no_list:
        pass
    else:
        pages_status.setdefault(url, 0)


def next_url():
    """
    Finds the next url in the dictionary that hasn't been scanned and returns it
    """
    for k, v in pages_status.items():
        if v == 0:
            return get_full_url(k)
    input('No more pages to scan')


def main():
    """
    Starts the program.
    Stores completed pages in a list and stores completed status within a dictionary
    """
    # The first iteration of this function is completed outside of the loop as the home page is hard coded.
    # After the first iteration, the variable changes to "current_url" and can then be looped
    print('Starting Scrape...')
    c = 0
    current_url = start_url
    add_to_dictionary(current_url)

    while True:
        res = requests.get(current_url)
        if res.history:
            print(current_url, "Appears to be a redirect.")
            del pages_status[current_url]
            add_to_dictionary(res.url)
            current_url = next_url()
            continue

        print("Current Page: " + current_url)
        pages_status[current_url] = 1
        temp_page = page.Page(current_url)
        pages.append(temp_page)
        c = c + 1

        for n in temp_page.all_links:
            current_url = get_full_url(n)
            add_to_dictionary(current_url)

        current_url = next_url()

        # Setting a temporary limit on the number of times that the loop iterates
        if c == 100:
            break

    storage.upload_information(pages)


if __name__ == '__main__':
    main()
