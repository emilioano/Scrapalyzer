
#import for filesystem
import os
#imports for filefunctions, libraries for pics, modules, pytorch for tensor/ML
import shutil
from transformers import AutoModelForImageClassification, AutoImageProcessor
from PIL import Image
import torch

#defines map for analyzed pics, creates if it doesnt exist, submap for pics without match
analyzed_path = 'data/analyzed/'
os.makedirs(analyzed_path, exist_ok=True)

nomatch_path = 'data/analyzed/zero_matches/'


class ImageAnalyzer:
    
    #constructor
    def __init__(self, model_name=""):

        #load pretrained model from huggingface, load picprocesser, deciding GPU / CPU
        self.model = AutoModelForImageClassification.from_pretrained('modules/analyzer/models/vit-base-patch16-224',local_files_only=True)
        self.processor = AutoImageProcessor.from_pretrained('modules/analyzer/models/vit-base-patch16-224',local_files_only=True)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        #moving model to chosen device and puts in evaluation-state
        self.model.to(self.device)
        self.model.eval()


    
    #defining method, path as input
    def classify_image(self, image_path):

        #open pic, convert to RGB for consitency, pytorch-tensor analyze pic w processor
        #moves tensor to correct device, runs pic to receive logit values, extracts logits
        try:
            image = Image.open(image_path).convert("RGB")
            inputs = self.processor(images=image, return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits
            #convert to probabilities, highest confidence w index, mapping index, extracting confidencevalue    
            probabilities = torch.softmax(logits, dim=1)
            top_prob, top_idx = torch.max(probabilities, dim=1)
            predicted_label = self.model.config.id2label[top_idx.item()]
            confidence = top_prob.item()
            #returning results as dictionary
            print(f'Predicted label: {predicted_label}')
            return {
                "label": predicted_label,
                #confidence": confidence,
                "error": None
            }
        #errormessage if invalid
        except Exception as e:
            return {
                "label": None,
                #"confidence": None,
                "error": f"Error classifying image {image_path}: {str(e)}"
            }
    #defining method which analyzes directory and sorts pictures
    def analyze_images(self, analysed_dir, keywords):
        #starting message
        print('Starting analyze_images')

        #initializing a list to save results
        results = []
        nokeyword = False

        #looping through all files in directory, building searchable files
        for filename in os.listdir(analysed_dir):
            print(f'Filename: {filename}')
            if filename.lower().endswith(('.png', '.jpg', '.jpeg','.webp')):
                image_path = os.path.join(analysed_dir, filename)
                print(f'Image path: {image_path}')
                #call classifying method, put result in list
                result = self.classify_image(image_path)
                result["filename"] = filename
                results.append(result)

                #checking if there is no error, get raw label, replacing "_" and " "
                if result.get("error") is None:
                    labelraw = result.get("label", "").lower()
                    label = labelraw.replace(',',' -')
                    #printing classification and path
                    print(f'Identification done in in {filename}, object is identified as {label}!')
                              
                    #assigning keywords if label is empty, with a message
                    if not keywords:
                        keywords = [label.replace(',',' -')]
                        nokeyword = True
                        print(f'Keyword was empty, keyword is now {keywords}')
                    
                    #looping through keywords, moving file to corresponding folder based on keyword.
                    for keyword in keywords:
                        fullpath=os.path.join(analyzed_path, keyword)

                        if keyword in label:
                            os.makedirs(analyzed_path+keyword, exist_ok=True)
                            print(f'Folder {analyzed_path}{keyword} exists or is now created!')

                            shutil.move(image_path, os.path.join(fullpath, filename))
                            print(f'Keyword {keyword} was found in label {label}. Moved to {fullpath}{filename}')
                        else:
                            print(f'Keyword {keyword} not found in the label: {label}')
                    #nullify keywords if generated
                    if nokeyword:
                        keywords = []

        #moving the files that are left to nomatch_path
        for filename in os.listdir(analysed_dir):
            os.makedirs(nomatch_path, exist_ok=True)
            print(f'Folder {nomatch_path} for no matched object exists or is now created!')
            shutil.move(os.path.join(analysed_dir, filename), os.path.join(nomatch_path, filename))
            print(f'No match for object based on keywords, moved {filename} to {nomatch_path}')

        return 'Done' #result