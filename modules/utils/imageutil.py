import os
import requests
import cv2

import torch
import numpy as np

from torchvision.models.detection import maskrcnn_resnet50_fpn
from torchvision.models.detection.mask_rcnn import MaskRCNN_ResNet50_FPN_Weights
from torchvision.transforms import functional as F


import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


download_folder='data/downloads/'
os.makedirs(download_folder, exist_ok=True)

processed_folder='data/processed/'
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

    weights = MaskRCNN_ResNet50_FPN_Weights.DEFAULT
    model = maskrcnn_resnet50_fpn(weights=weights)
    model.eval()

    object_counter=1

    for file in os.listdir(download_folder):
        full_download_path = download_folder+file
        
        image = cv2.imread(full_download_path)

        if image is None:
            print('Could not load any picture')
            continue

        height,width = image.shape[:2]
        print(f'Loaded Image {file} Width is {width}, height is {height}')
        
        # Object segmentation
        image_rgb = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        image_tensor = F.to_tensor(image_rgb).unsqueeze(0)

        # Don't trace gradients, better performance
        with torch.no_grad():
            prediction = model(image_tensor)[0]



        # Defining of objects in image
        for i in range(len(prediction['scores'])):
            if prediction['scores'][i] > 0.80:
                mask = prediction["masks"][i, 0].cpu().numpy()
                mask_binary = mask > 0.5                
        
            # Creating new image with segmentet object only
            object = np.zeros_like(image_rgb)
            object[mask_binary] = image_rgb[mask_binary]

            # Cropping object to its bounding box
            y_indices, x_indices = np.where(mask_binary)
            if y_indices.size > 0 and x_indices.size > 0:
                y_min, y_max = y_indices.min(), y_indices.max()
                x_min, x_max = x_indices.min(), x_indices.max()
                object_crop = object[y_min:y_max+1, x_min:x_max+1]
                object_width = x_max-x_min
                object_height = y_max-y_min
                print(f'Object {object_counter}. Height: {object_height}. y_min: {y_min}, y_max: {y_max}')
                print(f'Object {object_counter}. Width: {object_width}. y_min: {x_min}, y_max: {x_max}')

                #Save object as separate image
                object_bgr = cv2.cvtColor(object_crop, cv2.COLOR_RGB2BGR)

                #Adding identifier to file name in case 'id' is inserted as argument
                if id is None:
                    full_processed_path = processed_folder+'object_'+str(object_counter)+'_'+file
                else:
                    full_processed_path = processed_folder+id+'_'+'object_'+str(object_counter)+'_'+file

                #Resize the image in case it's larger than predefined size in pixels
                if object_width > size or object_height > size:
                    if object_width >= object_height:
                        calculate_height=int(object_height/object_width*size)
                        print(f'Object {object_counter}. Height: {object_height}, object width: {object_width}. Calculate height: {calculate_height}')
                        object_resized = cv2.resize(object_bgr, (size,calculate_height))
                        print(f'Object {object_counter}. Detected horinsontally aligned cropped image with size larger than {size} pixels, adjusted to width: {size} and height: {calculate_height}.')
                    else:
                        calculate_width=int(object_width/object_height*size)
                        object_resized = cv2.resize(object_bgr, (calculate_width,size))
                        print(f'Object {object_counter}. Detected vertically aligned cropped image with sized larger than {size} pixels, adjusted to width: {calculate_width} and height {size}.')
                else:
                    object_resized=object_bgr

                save = cv2.imwrite(full_processed_path,object_resized)

                if save:
                    print(f'Object {object_counter}. Image {full_processed_path} saved')

                else:
                    print(f'No image saved in {full_processed_path}')

                object_counter+=1

            #Clean download folder
            #os.remove(full_download_path)
            #print(f'Image {full_download_path} removed')
        
'''
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
'''

#imagedownloader('https://st4.depositphotos.com/27201292/40335/i/1600/depositphotos_403356616-stock-photo-vertical-shot-path-forest.jpg')
#imageprocessor()