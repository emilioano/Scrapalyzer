import os
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from PIL import Image

#Class for the scraper function
class Scraper:
  #The constructor for the whole program
  def __init__(self, url):
      self.url = url
      self.urls = []
      self.extracted = []
    
#Function for fetching images from given URL
  def fetch_image(self):
     page = requests.get(self.url)
     soup = BeautifulSoup(page.text,"html.parser")
     images = soup.find_all('img')
     for img in images:
        self.urls.append(img.get('src'))
     return self.urls



#Function for extracting image
  def extract_image(self):
     
    







#Function for saving image to /downloads