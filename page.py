import re
import bs4
import requests
import scraper

class Page(object):
    def __init__(self, page_url):
        self.page_url = page_url
        self.page_text = ""
        self.title_text = ""
        self.title_length = len(self.title_text)
        self.h_tags = {}
        self.alt_text = {"With Alt": 0, "Without Alt": 0}
        self.anchors = 0
        self.all_links = []
        self.initiate_page()

    def initiate_page(self):
        """
        Calls the various functions to set the values within the Page class
        """
        self.get_page_text()
        self.scrape_title_tags()
        self.scrape_h_tags()
        self.scrape_alt_text()
        self.scrape_anchor_text()

    def get_page_text(self):
        """
        Takes the URL and gets the text from the page associated to the URL
        """
        res = requests.get(self.page_url)
        try:
            res.raise_for_status()
            self.page_text = bs4.BeautifulSoup(res.text, 'html.parser')
        except Exception as exc:
            print("There was an error in getting page text.\nError:", exc)

    def scrape_title_tags(self):
        """
        Takes the page text and finds the header text associated.
        These values are then stored in a dictionary
        """
        try:
            self.title_text = self.page_text.select('title')[0].get_text()
        except Exception as exc:
            print('Current Page is missing title text.\nError: ', exc)

    def scrape_h_tags(self):
        """
        Takes the page text and finds the h tags
        Each h tag is added to a dictionary and the values totalled up
        """
        try:
            h1_tags = self.page_text.select('h1')
            for n in h1_tags:
                self.h_tags.setdefault(str(n)[1:3], 0)
                self.h_tags[str(n)[1:3]] += 1
        except Exception as exc:
            print('There are no head tags on current page.\nError: ', exc)

    def scrape_alt_text(self):
        """
        Takes the page text and finds the images
        Dictionary values increased depending on whether the image has alt text or not
        """
        image_code = self.page_text.select('img')
        for n in range(len(image_code)):
            if image_code[n].get('alt') == "":
                self.alt_text["Without Alt"] += 1
            else:
                self.alt_text["With Alt"] += 1

    def scrape_anchor_text(self):
        """
        Takes the page text and finds the anchor text on links. Ignores links that are images and not text
        Looks up the text against a list of generic text and adds up each time the text is in the list
        Note: For SEO purposes, Google only really cares about the first link, so this will only evaluate the first link
        """
        bad_anchors_text = ['read more', 'click here', 'here', 'see more', 'learn more', 'find out more']
        bad_anchors_logged = 0
        links = self.page_text.select('a')
        links_logged = []
        anchors = {}

        for n in links:

            link_regex = re.compile(r'\?.*|/en/|http.*|mailto:.*|#')
            mo = link_regex.sub("", n.get('href'))
            if mo != "":
                if mo not in links_logged and mo != 'javascript:void(0)':
                    links_logged.append(n.get('href'))
                    # This code is not needed unless we want to report on all anchors, not just bad anchors
                    # anchors[n.get('href')] = n.get_text().replace('\n', '')
                    if n.get_text().replace('\n', '').lower() in bad_anchors_text:
                        bad_anchors_logged += 1
                        # remove next (1) line if decide to report on all anchors
                        anchors[n.get('href')] = n.get_text().replace('\n', '')
        self.anchors = {'Bad Anchors': bad_anchors_logged}

    def get_all_links(self):
        links = self.page_text.select('a')
        links_logged = []

        for n in links:
            link_regex = re.compile(r'\?.*|/en/|http.*|mailto:.*|#')
            mo = link_regex.sub("", n.get('href'))
            if mo != "":
                if mo not in links_logged and mo != 'javascript:void(0)':

                    links_logged.append(scraper.get_full_url(mo))

        return links_logged
