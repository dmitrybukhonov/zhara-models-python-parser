import os
import requests
from urllib.parse import urlparse

def download_image(url, base_directory):
    parsed_url = urlparse(url)
    path_components = parsed_url.path.split('/')
    
    current_directory = base_directory
    for component in path_components[:-1]:
        current_directory = os.path.join(current_directory, component)
        os.makedirs(current_directory, exist_ok=True)
    
    filename = os.path.join(current_directory, path_components[-1])
    
    response = requests.get(url)
    if response.ok:
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Изображение загружено в {filename}")
    else:
        print("Не удалось загрузить изображение")
