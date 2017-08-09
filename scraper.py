import bs4
import requests
import re

# chromedriver = "C:\\Users\\Richard\\Documents\\Programs\\chromedriver.exe"

url = "http://www.tearfund.org/en/about_you/what_your_church_can_do/"
print('Starting Scrape...')
print('Setting homepage to %s...' % (url))

pages_scraped = {}

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
    """
    Takes the page text passed through and finds the anchor text on links
    Ignores links that are images and not text
    Looks up the text against a list of generic text and adds up each time the text is in the list
    Note: For SEO purposes, Google only really cares about the first link, so this will only evaluate the first link
    Returns the amount of links with text matching to the text in the list and the bad anchor text
    """
    bad_anchors = ['read more', 'click here', 'here', 'see more', 'learn more', 'find out more']
    bad_anchors_logged = 0
    links = page_text.select('a')
    links_logged = []
    anchors = {}

    for n in links:
        link_regex = re.compile(r'\?.*|\/en\/|http.*|mailto:.*')
        mo = link_regex.sub("", n.get('href'))
        if mo != "":
            if mo not in links_logged and mo != 'javascript:void(0)':
                # send the link over to store_links to prevent replication of loop
                store_links(n.get('href'))
                links_logged.append(n.get('href'))
                # This code is not needed unless we want to report on all anchors, not just bad anchors
                # anchors[n.get('href')] = n.get_text().replace('\n', '')
                if n.get_text().replace('\n', '').lower() in bad_anchors:
                    bad_anchors_logged += 1
                    # remove next (1) line if decide to report on all anchors
                    anchors[n.get('href')] = n.get_text().replace('\n', '')

            else:
                print(n.get('href'), "has already been recorded or is an invalid url")

    print('Print there are: ', str(bad_anchors_logged), ' bad anchors')


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


def store_links(url):
    """
    Takes the page text passed through and finds all the links
    Checks whether the link is an internal link and if not ignores it
    If not already part of dictionary, adds it and sets default value to 0
    Value should only ever be set to 1 if the page is scraped
    """
    # print(url)
    pass


def check_page_level():
    # not sure how to do this one yet - but need to store the minimum number of clicks to get to page
    pass


def scrape_all(page_text):
    page_list = [scrape_title_tags(page_text), scrape_h_tags(page_text), scrape_alt_text(page_text)]
    print(page_list)

    scrape_anchor_text(page_text)


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


