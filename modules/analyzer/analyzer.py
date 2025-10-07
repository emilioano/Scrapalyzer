import os

import shutil
from transformers import AutoModelForImageClassification, AutoImageProcessor
from PIL import Image
import torch




analyzed_path = 'data/analyzed/'
os.makedirs(analyzed_path, exist_ok=True)

nomatch_path = 'data/analyzed/nomatch/'





class ImageAnalyzer:
    '''
    def init(self, model_name=""):
        """test"""
        pass
    
    def analyze_images(self, analysed_dir, cats_dir, dogs_dir):
        """analysed results in cats or dogs"""
        pass

    def classify_image(self, image_path):
        """Classify a single image and return the predicted label and confidence."""
        pass
    '''
    
    def __init__(self, model_name=""):
        """
        Initialize the analyzer with a pre-trained model from Hugging Face.
        Args:
            model_name (str): Name of the pre-trained model from Hugging Face.
        """

        self.model = AutoModelForImageClassification.from_pretrained('modules/analyzer/models/vit-base-patch16-224',local_files_only=True)
        self.processor = AutoImageProcessor.from_pretrained('modules/analyzer/models/vit-base-patch16-224',local_files_only=True)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.model.eval()


    

    def classify_image(self, image_path):
        """
        Classify a single image and return classification.
        Args:
            image_path (str): Path to the image file.
        Returns:
            dict: Dictionary with predicted classification or potential error
        """
        try:
            image = Image.open(image_path).convert("RGB")
            inputs = self.processor(images=image, return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits
            probabilities = torch.softmax(logits, dim=1)
            top_prob, top_idx = torch.max(probabilities, dim=1)
            predicted_label = self.model.config.id2label[top_idx.item()]
            confidence = top_prob.item()
            print(f'Predicted label: {predicted_label}')
            return {
                "label": predicted_label,
                #confidence": confidence,
                "error": None
            }
        except Exception as e:
            return {
                "label": None,
                #"confidence": None,
                "error": f"Error classifying image {image_path}: {str(e)}"
            }

    def analyze_images(self, analysed_dir, keywords):
        print('Starting analyze_images')
        """
        Analyze all images in analysed_dir and move them to cats_dir or dogs_dir.
        Args:
            analysed_dir (str): Directory with analysed images.
            cats_dir (str): Directory to store cat images.
            dogs_dir (str): Directory to store dog images.
        Returns:
            list: List of dictionaries with classification results.
        """
        # Creating folders corresponding to keywords entered
        #for keyword in keywords:
        #    os.makedirs(analyzed_path+keyword, exist_ok=True)
        #    print(f'Folder {analyzed_path}{keyword} exists or is now created!')

        os.makedirs(nomatch_path, exist_ok=True)
        print(f'Folder {nomatch_path} for no matched object exists or is now created!')
                        


        results = []

        for filename in os.listdir(analysed_dir):
            print(f'Filename: {filename}')
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(analysed_dir, filename)
                print(f'Image path: {image_path}')
                result = self.classify_image(image_path)
                result["filename"] = filename
                results.append(result)

                if result.get("error") is None:
                    label = result.get("label", "").lower()
                    print(f'Identification done in in {filename}, object is identified as {label}!')
                    

                    #Moving file to corresponding folder based on keyword.
                    for keyword in keywords:
                        fullpath=os.path.join(analyzed_path, keyword)

                        if keyword in label:
                            
                            os.makedirs(analyzed_path+keyword, exist_ok=True)
                            print(f'Folder {analyzed_path}{keyword} exists or is now created!')

                            shutil.move(image_path, os.path.join(fullpath, filename))
                            print(f'Keyword {keyword} was found in label {label}. Moved to {fullpath}{filename}')
                        else:
                            print(f'Keyword {keyword} not found in the label: {label}')

        #Moving the files that are left to nomatch_path
        for filename in os.listdir(analysed_dir):
            shutil.move(os.path.join(analysed_dir, filename), os.path.join(nomatch_path, filename))
            print(f'No match for object based on keywords, moved {filename} to {nomatch_path}')

            '''
                    if "cat" in label:
                        shutil.move(image_path, os.path.join(cats_dir, filename))
                        print(f'Saved {cats_dir}{filename}')
                    elif "dog" in label:
                        shutil.move(image_path, os.path.join(dogs_dir, filename))
                        print(f'Saved {dogs_dir}{filename}')
                    else:
                        result["error"] = f"Unexpected label: {result['label']}"
            '''
        return 'Done' #result


'''     
if __name__ == "__main__": # type: ignore
    analyzer = ImageAnalyzer()
    results = analyzer.analyze_images(
        analysed_dir="../../data/processed",
        cats_dir="../../data/analyzed/cats",
        dogs_dir="../../data/analyzed/dogs"
    )
    for result in results:
        print(result)
'''

'''
    analyze_images(
        analysed_dir="../../data/processed",
        cats_dir="../../data/cats",
        dogs_dir="../../data/dogs"
    )
'''