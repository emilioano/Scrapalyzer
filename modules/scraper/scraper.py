from urllib.parse import urljoin, urlparse
import os
from io import BytesIO

import requests
from bs4 import BeautifulSoup
from PIL import Image


#Class for the scraper function
class Scraper:
   def __init__(self, url):
      self.url = url
      self.urls = []
      self.extracted = []

    
#Function for fetching images from given URL
   def fetch_image(self):
     #Assigning values to variables so its easier to use bs4
     page = requests.get(self.url)
     soup = BeautifulSoup(page.text,"html.parser")
     images = soup.find_all('img')
     #Going through every img tag, grabbing its 'src' and adding it to my self.urls list
     for img in images:
        self.urls.append(img.get('src'))
     return self.urls



#Function for extracting image
   def extract_image(self):
    #Setting a variable so it filters out bad links/urls
    allowed_formats = ['.jpg', '.jpeg', '.png', '.webp']
    for link in self.urls:
       #If the link contains the allowed format then its appended to the self.extracted list
       if any(fmt in link for fmt in allowed_formats):
          self.extracted.append(link)
    


#Function for saving image to /
   def save_image(self):
    try:
       #Created the directory and if it already exists then, OK!
       os.makedirs('data/downloads', exist_ok=True)
       print('Directory is ready!')
    #Simple error handling
    except OSError as error:
       print('Failed to create directory!')
    #Looping through each link, adding different file-numbers for each file and also IF the specific url is too slow then it skips it
    for link in self.extracted:
        response = requests.get(link, timeout=10)
        filename = link.split('/') [-1]
        save_path = os.path.join('data/downloads', filename)
        #If the response is successful, we save the image to the specified path
        if response.status_code == 200:
           image = Image.open(BytesIO(response.content))
           image.save(save_path)
        else:
           continue
           
   def run(self, url_to_scrape):
      self.fetch_image()
    # Join urls
      self.urls = [urljoin(url_to_scrape, u) for u in self.urls if u]
    # Filter out unwanted urls
      self.urls = [
        u for u in self.urls
        if urlparse(u).scheme in ('http', 'https')
      ] 
    # Call functions to extract and scrape images
      self.extract_image()
      self.save_image()