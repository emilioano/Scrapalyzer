import os
import requests
import cv2

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Animal:
    def __init__(self):
        pass


download_folder='../downloads/'
os.makedirs(download_folder, exist_ok=True)

folder_cat='../cats/'
os.makedirs(folder_cat, exist_ok=True)

folder_dog='../dogs/'
os.makedirs(folder_dog, exist_ok=True)

savedpath=''

def imagedownloader(url,animal):
    file_name=os.path.basename(url)
    weburl=requests.get(url, verify=False)
    try:
        with open(os.path.join(download_folder, file_name), 'wb') as save:
            save.write(weburl.content)
        savedpath=download_folder+file_name
        print(f'Saved file as {savedpath}.')
        imagehandler('foggel',folder_cat,animal,savedpath)
    except Exception as issue:
        print(f'Did not succeed with {file_name}, that was downloaded from {url}. Issue is {issue}.')
    

def imagehandler(filename,path,animal,savedpath):
    #print('Filename: ', filename)
    #print('Path: ', path)
    #print('Animal: ', animal)
    #print('Path+Filename: ', path+filename+'.jpg')

    image = cv2.imread(savedpath)
    if image is None:
        print('Could not load any picture')

    resize_image = cv2.resize(image, (512,512))
    fullpath=path+filename+'.jpg'
    save = cv2.imwrite(fullpath,resize_image)

    if save:
        print(f'Image {fullpath} saved')
    else:
        print(f'No image saved in {fullpath}')

imagedownloader('https://cdn.prod.website-files.com/60e4d0d0155e62117f4faef3/621531f8df76222362702e67_jeremy-hynes-B_12uv-QLHY-unsplash-DeNoiseAI-severe-noise.jpg','cat')
