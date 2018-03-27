import page
import requests
import storage

domain = "https://www.tearfund.org"
start_url = 'https://www.tearfund.org/'

# List and dictionary to store Page class items and url status
pages = []
pages_status = {}

# Storing the headlines in a dictionary to see whether there is any duplication of headlines
all_titles = {}

def get_full_url(url):
    """
    Takes the page text passed through and finds all the links
    Checks whether the link is an internal link and if not ignores it
    If not already part of dictionary, adds it and sets default value to 0
    Value should only ever be set to 1 if the page is scraped
    """
    url = clean_url(url)
    if url[0:4] == "/en/":
        url = domain + url[4:]
    elif url[0] == "/":
        url = domain + url
    elif url[0:3] == "www":
        url = "https://" + url
    elif url[0:4] == "http" and url[0:5] != "https":
        url = "https" + url[4:]
    elif url[0:5] != "https":
        url = domain + "/" + url
    return url


def clean_url(url):
    """
    TODO: This needs to remove query strings from the url
    """

    return url.split('?', maxsplit=1)[0]


def add_to_dictionary(url):
    """
    Takes the url and checks to see whether it is a pdf or another file type
    These types of files will have issues being scanned so are cleaned out by this function
    """
    no_list = [".pdf", "pdf/", ".doc", "docx", ".ppt", "pptx"]
    if url[-4:] in no_list or url[:24] != "https://www.tearfund.org":
        # print('Will not add ' + url + ' to dictionary')
        pass
    else:
        pages_status.setdefault(url, 0)
        # print ('Adding ' + url + ' to dictionary')


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
        # Checks if the page is a redirect
        # If it is, it adds the new page to the dictionary and removes the redirect
        if res.history:
            print(str(c + 1), current_url, ": Appears to be a redirect.")
            del pages_status[current_url]
            add_to_dictionary(res.url)
            current_url = next_url()
            continue

        print(str(c + 1) + ": Current Page: " + current_url)
        pages_status[current_url] = 1
        temp_page = page.Page(current_url)
        pages.append(temp_page)

        # Gets the page title and stores it in a dictionary, noting the amount of occurrences of the title
        page_title = temp_page.title_text
        all_titles.setdefault(page_title, 0)
        all_titles[page_title] += 1

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
