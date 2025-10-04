import os
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from PIL import Image

url = 'https://pixabay.com/sv/images/search/animal/'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

#Function for fetching image from url
def fetch_image():
    images = soup.find_all('img')
    for img in images:
        print(img.get('src'))


#Function for extracting image


#Function for saving image