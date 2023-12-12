import requests
from config import DOMAIN
from bs4 import BeautifulSoup

class ModelParticipantsExtractor:
    def __init__(self, url):
        self.url = url
        self.section_links = []

    def get_section_links(self):
        with requests.get(self.url) as response:
            if response.ok:
                soup = BeautifulSoup(response.content, 'html.parser')
                links = soup.find_all('a', class_='csmx-media effect-hover')
                self.section_links = [
                    DOMAIN + link.get('href') for link in links if link.get('href')
                ]

        return self.section_links
