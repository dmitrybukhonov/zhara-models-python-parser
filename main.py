import requests

import json
import logging
from config import DOMAIN
from parsers.model_parser import ModelParser
from parsers.model_sections_extractor import ModelSectionsExtractor
from parsers.model_participants_extractor import ModelParticipantsExtractor

def fetch_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        with requests.get(DOMAIN, headers=headers) as response:
            if response.status_code == 200:
                return response.text
            else:
                print(f"Ошибка при получении страницы: {response.status_code}")
                return None
    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return None

def get_model_data_list(model_href_list):
    model_data_list = []
    for url in model_href_list:
        model_data = ModelParser(url).parse()

        if model_data:
            model_data_list.append(model_data)
    return model_data_list

def save_to_json(model_data_list, category):
    json_file = f'json/model_{category}_data.json'
    with open(json_file, 'w') as file:
        json.dump(model_data_list, file, ensure_ascii=False, indent=4)

def parse_data(html):
    section_links = ModelSectionsExtractor(html).get_section_links()

    for section_link in section_links:
        href = DOMAIN + section_link
        model_href_list = ModelParticipantsExtractor(href).get_section_links()

        model_data_list = get_model_data_list(model_href_list)

        category = section_link.strip('/')
        save_to_json(model_data_list, category)

def run_parser():
    try:
        html_data = fetch_data()
        if html_data:
            parse_data(html_data)
    except Exception as e:
        logging.exception("Ошибка во время выполнения парсера: %s", e)
def main():
    run_parser()

if __name__ == "__main__":
    main()
