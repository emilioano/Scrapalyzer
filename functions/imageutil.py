import os
import requests
import cv2

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

download_folder='../downloads/'
os.makedirs(download_folder, exist_ok=True)
folder_cats='dogs/'
folder_dogs='cats/'

def imagedownloader(url):
    file_name=os.path.basename(url)
    weburl=requests.get(url, verify=False)
    try:
        with open(os.path.join(download_folder, file_name), 'wb') as save:
            save.write(weburl.content)
        print(f'Saved file as {download_folder}{file_name}.')
    except Exception as issue:
        print(f'Did not succeed with {file_name}, that was downloaded from {url}. Issue is {issue}.')
    


#def imagehandler(url, animal, filename):
#    pass
    #try:
        #pass
        

imagedownloader('https://cdn.prod.website-files.com/60e4d0d0155e62117f4faef3/621531f8df76222362702e67_jeremy-hynes-B_12uv-QLHY-unsplash-DeNoiseAI-severe-noise.jpg')