import re
import bs4
import requests


class Page(object):
    def __init__(self, page_url):
        self.page_url = self.set_full_url(page_url)
        self.page_content = ""
        self.page_text = ""
        self.title_text = ""
        self.title_length = 0
        self.h_tags = {}
        self.alt_text = {"With Alt": 0, "Without Alt": 0}
        self.anchors = 0
        self.all_links = []
        self.initiate_page()

    def initiate_page(self):
        """
        Calls the various functions to set the values within the Page class
        """
        self.get_page_content()

        self.scrape_title_tags()
        self.title_length = len(self.title_text)
        self.scrape_h_tags()
        self.scrape_alt_text()
        self.scrape_anchor_text()
        self.get_all_links()
        self.get_page_text()

    def get_page_content(self):
        """
        Takes the URL and gets the text from the page associated to the URL
        """
        res = requests.get(self.page_url)
        try:
            res.raise_for_status()
            self.page_content = bs4.BeautifulSoup(res.text, 'html.parser')
        except Exception as exc:
            pass

    def scrape_title_tags(self):
        """
        Takes the page text and finds the header text associated.
        These values are then stored in a dictionary
        """
        try:
            self.title_text = self.page_content.select('title')[0].get_text()
        except Exception as exc:
            pass

    def scrape_h_tags(self):
        """
        Takes the page text and finds the h tags
        Each h tag is added to a dictionary and the values totalled up
        """
        try:
            h1_tags = self.page_content.select('h1')
            for n in h1_tags:
                self.h_tags.setdefault(str(n)[1:3], 0)
                self.h_tags[str(n)[1:3]] += 1
        except Exception as exc:
            pass

    def scrape_alt_text(self):
        """
        Takes the page text and finds the images
        Dictionary values increased depending on whether the image has alt text or not
        """
        image_code = self.page_content.select('img')
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
        links = self.page_content.select('a')
        links_logged = []
        for n in links:
            try:
                link_regex = re.compile(r'\?.*|/en/|http.*|mailto:.*|#')
                mo = link_regex.sub("", self.set_full_url(n.get('href')))

                if mo != "":
                    if mo not in links_logged and mo != 'javascript:void(0)':
                        links_logged.append(n.get('href'))
                        # This code is not needed unless we want to report on all anchors, not just bad anchors
                        # self.anchors += 1
                        if n.get_text().replace('\n', '').lower() in bad_anchors_text:
                            self.anchors += 1
            except Exception as exc:
                continue

    def get_all_links(self):
        """
        Takes the page text and finds all the link urls
        This can then be stored and cross referenced to find other pages for the program to crawl
        """
        links = self.page_content.select('a')
        for n in links:

            try:
                link_regex = re.compile(r'\?.*|http.*|mailto:.*|#.*')
                mo = link_regex.sub("", self.set_full_url(n.get('href')))

                link_regex = re.compile(r'/en/')
                mo = link_regex.sub("/", mo)

                if mo != "":
                    if mo not in self.all_links and mo != 'javascript:void(0)':
                        mo = self.set_full_url(mo)
                        self.all_links.append(mo)
            except Exception as exc:
                continue

    def set_full_url(self, url):
        """
        Takes the page text passed through and finds all the links
        Checks whether the link is an internal link and if not ignores it
        If not already part of dictionary, adds it and sets default value to 0
        Value should only ever be set to 1 if the page is scraped
        """
        if url[0] != "/" and url[0:4] != "http" and url[0:3] != "www":
            url = "http://www.tearfund.org/" + url
        if url[0] == "/":
            url = "www.tearfund.org" + url
        elif url[0:4] != "http" and url[0:3] != "www":
            url = "www.tearfund.org/" + url
        return url

    def get_page_text(self):
        """
        Takes the text and grabs out the content within the body tag.
        Then strips out any text within <> tafs
        """

