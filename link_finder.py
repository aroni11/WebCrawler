import requests
from bs4 import BeautifulSoup


class LinkFinder:

    def __init__(self, base_url, page_url):
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()

    def get_links(self):
        res = requests.get(self.page_url)
        source = BeautifulSoup(res.text, 'html.parser')
        for link in source.findAll('a'):
            if link.get('href').startswith('/'):
                self.links.add(self.base_url + link.get('href'))
            else:
                self.links.add(link.get('href'))
        return self.links
