import bs4
import requests

# chromedriver = "C:\\Users\\Richard\\Documents\\Programs\\chromedriver.exe"

url = "http://www.tearfund.org"
print('Starting Scrape...')
print('Setting homepage to %s...' % (url))


def scrape_title_tags(page_text):
    """
    Takes the page text passed through and finds the header text and length associated.
    These values are then stored in a dictionary
    If there is no header text, the dictionary has blank fields added
    Returns the dictionary
    """
    try:
        title_text = page_text.select('title')[0].get_text()
        title_length = len(title_text)
        title_dict = {'Title': title_text, 'Length': title_length}
    except Exception as exc:
        print('Page ', url, ' is missing title text\nError: ', exc)
        title_dict = {'Title': '', 'Length': 0}
    return title_dict


def scrape_h_tags(page_text):
    """
    Takes the page text passed through and finds the h tags
    Each h tag is added to a dictionary and the values totalled up
    If no h tags, the dictionary is left blank
    Returns the dictionary
    """
    tag_dictionary = {}
    try:
        h1_tags = page_text.select('h1')
        for n in h1_tags:
            tag_dictionary.setdefault(str(n)[1:3], 0)
            tag_dictionary[str(n)[1:3]] += 1
    except Exception as exc:
        print('There are no head tags on page ', url, '\nError: ', exc)
    return tag_dictionary


def scrape_anchor_text(page_text):
    # scrape url passed through to check the anchor link text
    pass


def scrape_alt_text(page_text):
    """
    Takes the page text passed through and finds the images
    Dictionary values increased depending on whether the image has alt text or not
    Returns the dictionary
    """
    image_code = page_text.select('img')
    alt_text = {"With": 0, "Without": 0}
    for n in range(len(image_code)):
        if image_code[n].get('alt') == "":
            alt_text["Without"] += 1
        else:
            alt_text["With"] += 1
    return alt_text


def check_page_level():
    # not sure how to do this one yet - but need to store the minimum number of clicks to get to page
    pass


def scrape_all(page_text):
    page_list = [scrape_title_tags(page_text), scrape_h_tags(page_text)]
    scrape_alt_text(page_text)
    print(page_list)
    pass


def store_results(the_results):
    # store the results in a google sheet
    pass


def main():
    res = requests.get(url)
    try:
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        scrape_all(soup)

        print('The page %s has been recorded' % (url))
    except Exception as exc:
        print("There was an error: %s \nThe url %s has been skipped" % (exc,url))


if __name__ == '__main__':
    main()


