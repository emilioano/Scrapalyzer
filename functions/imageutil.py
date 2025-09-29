import os
import requests
import cv2

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


download_folder='../downloads/'
os.makedirs(download_folder, exist_ok=True)

processed_folder='../processed/'
os.makedirs(processed_folder, exist_ok=True)

size = 512


def imagedownloader(url,id=None):
    file_name=os.path.basename(url)
    weburl=requests.get(url, verify=False)
    if file_name.endswith(('.jpg','.png','.jpeg')):
        try:
            with open(os.path.join(download_folder, file_name), 'wb') as save:
                save.write(weburl.content)
            saved_path=download_folder+file_name
            print(f'Saved file as {saved_path}.')
            imageprocessor(id)
        except Exception as issue:
            print(f'Did not succeed with {file_name}, from {url}. Issue is {issue}.')
    else:
        print(f'Unvalid format of {url}.')


def imageprocessor(id=None):
    for file in os.listdir(download_folder):
        full_download_path = download_folder+file
        
        if id is None:
            full_processed_path = processed_folder+file
        else:
            full_processed_path = processed_folder+id+'_'+file

        image = cv2.imread(full_download_path)

        height,width = image.shape[:2]
        print(f'Width is {width}, height is {height}')
        
        #print('Loading: ',full_download_path)
        if image is None:
            print('Could not load any picture')
            continue

        if width >= height:
            calculate_height=int(height/width*size)
            resize_image = cv2.resize(image, (size,calculate_height))
            print(f'Horinsontal image, saved with width: {size} and height: {calculate_height}.')
        else:
            calculate_width=int(width/height*size)
            resize_image = cv2.resize(image, (calculate_width,size))
            print(f'Vertical image, saved with width: {calculate_width} and height {size}.')

        save = cv2.imwrite(full_processed_path,resize_image)

        if save:
            print(f'Image {full_processed_path} saved')
            os.remove(full_download_path)
            print(f'Image {full_download_path} removed')
        else:
            print(f'No image saved in {full_processed_path}')


imagedownloader('https://cdn.pixabay.com/photo/2018/12/03/19/26/forest-3854077_1280.jpg')
