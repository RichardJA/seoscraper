import page
import storage
import requests
from collections import defaultdict
import time

domain = "https://www.tearfund.org"
start_url = 'https://www.tearfund.org/'

# List and dictionary to store Page class items and url status
pages = []
pages_status = {}

# Storing the headlines in a dictionary to see whether there is any duplication of headlines
# using defaultdict allows you to specify that the value in the dictionary is a list
all_titles = defaultdict(list)


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
            return k
        # Uncomment this when setting live for whole site
        # else:
            # return False
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
    sheet_connect = storage.connect_to_google_sheets()
    while True:
        start_time = time.time()
        res = requests.get(current_url)
        if res.history:
            del pages_status[current_url]
            add_to_dictionary(res.url)
            current_url = next_url()
            continue

        print(str(c + 1) + " - Current Page: " + current_url)

        pages_status[current_url] = 1
        temp_page = page.Page(current_url)
        pages.append(temp_page)

        # Gets the page title and stores it in a dictionary, noting the amount of occurrences of the title
        page_title = temp_page.title_text
        all_titles[page_title].append(temp_page.page_url)

        for n in temp_page.all_links:
            add_to_dictionary(n)

        current_url = next_url()

        # If there are no further pages, current_url should be false
        # As such break out of the loop
        # Uncomment this when setting live for whole site
        if not current_url:
            break

        # This is used to create part of the temporary limit on crawls & to pass row for storage
        c = c + 1

        storage.upload_information(sheet_connect, temp_page, c)

        print("\tProcess Took: " + str(time.time() - start_time)[:6] + " seconds")

        # Setting a temporary limit on the number of times that the loop iterates
        # Uncomment if wanted to test over a smaller set of pages
        # if c == 999:
        #     break
    print("Scrape done. Scanned " + str(c + 1) + " pages!")


if __name__ == '__main__':
    main()
