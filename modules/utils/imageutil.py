#Abstract method
from abc import ABC, abstractmethod

# Logging library
import logging

# Libraries to handle files and images. os and OpenCV
import os
import cv2

# Libraries to use in relation to Mask R-CNN.
import torch
import numpy as np
from torchvision.models.detection import maskrcnn_resnet50_fpn
from torchvision.models.detection.mask_rcnn import MaskRCNN_ResNet50_FPN_Weights
from torchvision.transforms import functional as F

# Library for the analyzer model downloader
from huggingface_hub import snapshot_download

# Logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Initialize local model used for analyzer.
# Model url and files that is used for analyzer
model_dir = "modules/analyzer/models/vit-base-patch16-224"
needed_files = ["config.json", "pytorch_model.bin", "preprocessor_config.json"]

# Download if it's not existing
def downloadanalyzermodel():
    if not all(os.path.exists(os.path.join(model_dir, f)) for f in needed_files):
        snapshot_download(
            repo_id="google/vit-base-patch16-224",
            local_dir=model_dir,
        )


# Set where imagedownloader puts files.
download_folder='data/downloads/'
os.makedirs(download_folder, exist_ok=True)

# Set where imageprocessor puts processed files.
processed_folder='data/processed/'
os.makedirs(processed_folder, exist_ok=True)

# Set the max pixel size for saved object images. Pictures larger will be rezised to this, both width and height is considered.
size = 512

# Set the minimum object image pixel size that will be considered for further processing. Both width and height considered. 
min_size = 150

class ImageProcessor(ABC):
    def __init__(self, id=None):
        self.id = id

    @abstractmethod
    def imagehandler(self):
        pass

class ProcessImages(ImageProcessor):
    def imagehandler(self):

        #Mask R-CNN related variables
        weights = MaskRCNN_ResNet50_FPN_Weights.DEFAULT
        model = maskrcnn_resnet50_fpn(weights=weights)
        model.eval()

        # Giving each object an INT value
        object_counter=1

        # Loading the pictures using OpenCV and segmenting with Mask R-CNN 
        for file in os.listdir(download_folder):
            try:
                full_download_path = download_folder+file
                image = cv2.imread(full_download_path)

                if image is None:
                    logger.info('Could not load any picture')
                    continue

                height,width = image.shape[:2]
                logger.info(f'Loaded Image {file} Width is {width}, height is {height}')

                # Object segmentation
                image_rgb = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
                image_tensor = F.to_tensor(image_rgb).unsqueeze(0)

                # Don't trace gradients, better performance
                with torch.no_grad():
                    # model returns predictions.
                    prediction = model(image_tensor)[0]

            except Exception as error:
                logger.error(f'Error has occured: {error}')


            # Defining of objects in image
            for i in range(len(prediction['scores'])):
                try:
                    # If prediction scored over threshold value, then
                    if prediction['scores'][i] > 0.80:
                        mask = prediction["masks"][i, 0].cpu().numpy()
                        mask_binary = mask > 0.5                

                         # Creating new image with segmentet object only, Mask R-CNN related
                        object = np.zeros_like(image_rgb)
                        object[mask_binary] = image_rgb[mask_binary]

                        # Cropping object to its bounding box, Mask R-CNN related
                        y_indices, x_indices = np.where(mask_binary)
                        if y_indices.size > 0 and x_indices.size > 0:
                            y_min, y_max = y_indices.min(), y_indices.max()
                            x_min, x_max = x_indices.min(), x_indices.max()
                            object_crop = object[y_min:y_max+1, x_min:x_max+1]
                            object_width = x_max-x_min
                            object_height = y_max-y_min
                            logger.info(f'Object {object_counter}. Height: {object_height}. y_min: {y_min}, y_max: {y_max}')
                            logger.info(f'Object {object_counter}. Width: {object_width}. y_min: {x_min}, y_max: {x_max}')

                        #Save segmented object in separately
                        object_bgr = cv2.cvtColor(object_crop, cv2.COLOR_RGB2BGR)

                        #Adding identifier to file name in case an 'id' is inserted as argument
                        if self.id is None:
                            full_processed_path = processed_folder+'object_'+str(object_counter)+'_'+file
                        else:
                            full_processed_path = processed_folder+self.id+'_'+'object_'+str(object_counter)+'_'+file

                        #Resize the image in case it's larger than predefined size in pixels
                        if object_width > size or object_height > size:
                            if object_width >= object_height:
                                calculate_height=int(object_height/object_width*size)
                                logger.info(f'Object {object_counter}. Height: {object_height}, object width: {object_width}. Calculate height: {calculate_height}')
                                object_resized = cv2.resize(object_bgr, (size,calculate_height))
                                logger.info(f'Object {object_counter}. Detected horinsontally aligned cropped image with size larger than {size} pixels, adjusted to width: {size} and height: {calculate_height}.')
                            else:
                                calculate_width=int(object_width/object_height*size)
                                object_resized = cv2.resize(object_bgr, (calculate_width,size))
                                logger.info(f'Object {object_counter}. Detected vertically aligned cropped image with sized larger than {size} pixels, adjusted to width: {calculate_width} and height {size}.')
                        else:
                            object_resized=object_bgr

                        # Only save object images that are larger than the decided threshold
                        if object_resized.shape[0] > min_size and object_resized.shape[1] > min_size:
                            save = cv2.imwrite(full_processed_path,object_resized)
                        else:
                            logger.info(f'Object {object_counter}. Detected image with width or height smaller than {min_size} pixels. Not saving it.')
                            continue

                        if save:
                            logger.info(f'Object {object_counter}. Image {full_processed_path} saved')

                        else:
                            logger.info(f'No image saved in {full_processed_path}')

                        object_counter+=1
                    
                except Exception as error:
                    logger.error(f'Error has occured: {error}')


# Call this function to start processing
def imageprocessor(id=None):
    startprocessing = ProcessImages(id)
    startprocessing.imagehandler()