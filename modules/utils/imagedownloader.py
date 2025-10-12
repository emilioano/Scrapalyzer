#Abstract method
from abc import ABC, abstractmethod

# Import logger library
import logging

#Import file and web handler
import os
import requests

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Set where imagedownloader puts files.
download_folder='data/downloads/'
os.makedirs(download_folder, exist_ok=True)

class FileDownloader(ABC):
    def __init__(self, url, id=None):
        self.url = url
        self.id = id

    @abstractmethod    
    def filedownloader(self):
        pass

class ImageDownloader(FileDownloader):
    def filedownloader(self):
        file_name=os.path.basename(self.url)
        weburl=requests.get(self.url, verify=False)
        if file_name.endswith(('.jpg','.png','.jpeg','webp')):
            try:
                if self.id:
                    with open(os.path.join(download_folder, self.id+'_'+file_name), 'wb') as save:
                        save.write(weburl.content)
                        saved_path=download_folder+self.id+'_'+file_name
                else:
                    with open(os.path.join(download_folder, file_name), 'wb') as save:
                        save.write(weburl.content)
                        saved_path=download_folder+file_name
                    
                logger.info(f'Saved file as {saved_path}.')
            except Exception as error:
                logger.error(f'Did not succeed with {file_name}, from {self.url}. Issue is {error}.')
        else:
            logger.info(f'Unvalid format of {self.url}.')

# Call this function to download image
def downloader(url, id=None):
    downloader = ImageDownloader(url, id)
    downloader.filedownloader()

downloader('https://static.bonniernews.se/ba/16204c4d-c14f-47e5-a371-f7a97c79b541.jpeg','Ballen')