import logging
import os
import requests

logger = logging.getLogger(__name__)

# Set where imagedownloader puts files.
download_folder='data/downloads/'
os.makedirs(download_folder, exist_ok=True)

def imagedownloader(url,id=None):
    file_name=os.path.basename(url)
    weburl=requests.get(url, verify=False)
    if file_name.endswith(('.jpg','.png','.jpeg','webp')):
        try:
            with open(os.path.join(download_folder, file_name), 'wb') as save:
                save.write(weburl.content)
            saved_path=download_folder+file_name
            logger.info(f'Saved file as {saved_path}.')
        except Exception as error:
            logger.error(f'Did not succeed with {file_name}, from {url}. Issue is {error}.')
    else:
        logger.info(f'Unvalid format of {url}.')