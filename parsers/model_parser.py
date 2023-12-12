import requests
from config import DOMAIN
from bs4 import BeautifulSoup
from function.download_image import download_image

class ModelParser:
    def __init__(self, url):
        self.url = url
        self.model_data = {}

    def _get_html(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(self.url, headers=headers)
        return response.text if response.ok else None

    def _parse_model_name(self, soup):
        model_name_tag = soup.find('h1', class_='csmx-section-title entry-title csmx-align-left')
        self.model_data['Имя'] = model_name_tag.text.strip() if model_name_tag else None

    def _parse_model_table(self, soup):
        table = soup.find('table', class_='csmx-align-center')
        rows = table.find_all('tr') if table else []

        model_data = {}
        for index, row in enumerate(rows):
            columns = row.find_all(['th', 'td'])
            row_data = [col.text.strip() for col in columns]
            if index == 0:
                keys = row_data
            else:
                model_data = dict(zip(keys, row_data))

        self.model_data.update(model_data)

    def _parse_images(self, soup):
        image_links = []
        image_tags = soup.find_all('a', class_='csmx-media')
        for tag in image_tags:
            image_url = tag.get('href')
            download_image(DOMAIN + image_url, 'json')
            image_links.append(image_url)

        self.model_data['images'] = image_links

    def parse(self):
        html = self._get_html()
        if html:
            print(f'Парсинг страницы модели {self.url}')

            soup = BeautifulSoup(html, 'html.parser')
            self._parse_model_name(soup)
            self._parse_model_table(soup)
            self._parse_images(soup)

            return self.model_data
        else:
            print(f'Ошибка при получении страницы модели {self.url}')
            return None
