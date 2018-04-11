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
        print(page_url)

    def initiate_page(self):
        """
        Calls the various functions to set the values within the Page class
        """
        self.get_page_content()
        self.get_page_text()
        self.scrape_title_tags()
        self.title_length = len(self.title_text)
        self.scrape_h_tags()
        self.scrape_alt_text()
        self.scrape_anchor_text()
        self.get_all_links()

        return self.title_text

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


    def clean_page_text(self, text):
        """
        Takes the page text passed to it and cleans it
        Should be left with just the copy of the text
        Removes all tags and code
        """

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
                link_regex = re.compile(r'http.*|mailto:.*|#')
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
                # This used to be regex, however I have changed it to a bs4 selection
                # This is because I didn't think it was correctly working, nor was it the most efficient way

                # Prevents storing redirects
                res = requests.get(self.set_full_url(n.get('href')))
                url = res.url

                # Needs to be placed here as redirects can avoid this
                if url[-1] != "/":
                    url = url + "/"

                if res.url != "" and url not in self.all_links:
                    if self.check_valid_url(url):
                        #print("Approved: " + url)
                        self.all_links.append(url)
                    # else:
                        # print('Not Valid: ' + url)
                # else:
                    # print('Already in links: ' + url)

            except Exception as exc:
                continue

    def set_full_url(self, url):
        """
        Takes the page text passed through and finds all the links
        Checks whether the link is an internal link and if not ignores it
        """
        url = url.split('?', maxsplit=1)[0]
        url = url.split('#', maxsplit=1)[0]

        if url[0] == '#':
            return url

        if url[-1] != "/":
            url = url + "/"

        if url[0:4] != "http" and url[0] != "/":
            url = "/" + url

        if url[0:4] == '/en/':
            url = 'https://www.tearfund.org' + url[3:]
        elif url[0] == "/":
            url = 'https://www.tearfund.org' + url
        elif url[0:3] == "www":
            url = "https://" + url
        elif url[0:4] == "http" and url[0:5] != "https":
            url = "https" + url[4:]
        elif url[0:5] != "https":
            url = 'https://www.tearfund.org' + "/" + url

        return url

    def get_page_text(self):
        """
        Takes the text and grabs out the content within the body tag.
        Then strips out any text within <> tafs
        """

    def check_valid_url(self, url):
        """
        Checks whether the URL is a Tearfund URL and whether it is a valid webpage (eg not mailto)
        Returns False if invalid and True if valid
        """
        if url[0] == '#':
            return False

        # URLS that shouldn't be included in the scrape
        no_list = ["~", "/../", "/layouts/", "/admin/"]
        for word in no_list:
            if word in url:
                return False

        # Looking to see whether the match as an email address and excluding it if it is
        reg_email = re.compile(r'mailto:')
        match_object = reg_email.search(url)

        if match_object is not None:
            return False

        # Looking to see if the match is tearfund's own site, and excluding it if not
        reg_exernal_site = re.compile(r'https://www\.tearfund\.org')
        match_object = reg_exernal_site.search(url)

        if match_object is None:
            return False
        return True

