import os
from io import BytesIO
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from PIL import Image

#Variables to simulate a browser to bypass bot blockers on certain websites
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com",
    "Connection": "keep-alive" 
   
   
}


#Class for the scraper function
class Scraper:
   def __init__(self, url):
      self.url = url
      self.urls = []
      self.extracted = []

    
#Function for fetching images from given URL
   def fetch_image(self):
     #Assigning values to variables so its easier to use bs4
     page = requests.get(self.url, headers=headers)
     soup = BeautifulSoup(page.text,"html.parser")
     images = soup.find_all('img')
     #Going through every img tag, grabbing its 'src' and adding it to my self.urls list
     for img in images:
        src = img.get('src') or img.get('data-src')
        if src:
           self.urls.append(src)
     return self.urls



#Function for extracting image
   def extract_image(self):
    #Setting a variable so it filters out bad links/urls
    allowed_formats = ['.jpg', '.jpeg', '.png', '.webp']
    #'urljoin' guarantees that every URL becomes a valid URL (it adds missing protocol)
    self.urls = [urljoin(self.url, u) for u in self.urls if u]
    #Filter out unwanted urls, 'scheme' extracts just the scheme part ('https', 'https')
    self.urls = [
        u for u in self.urls
        if urlparse(u).scheme in ('http', 'https')
      ]    
    #Just to make sure list is clear before appending to avoid duplicates
    self.extracted.clear()
    for link in self.urls:
       #If the link contains the allowed format then its appended to the self.extracted list, .lower prevents the function from missing .JPG uppercases
       if any(fmt in link.lower() for fmt in allowed_formats):
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
        response = requests.get(link, timeout=100, headers=headers)
        filename = link.split('/') [-1]
        save_path = os.path.join('data/downloads', filename)
        #If the response is successful, we save the image to the specified path
        if response.status_code == 200:
           image = Image.open(BytesIO(response.content))
           image.save(save_path)
        else:
           continue
   #Run function        
   def run(self):
      self.fetch_image()
      self.extract_image()
      self.save_image()