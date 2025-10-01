import os
import shutil
from transformers import AutoModelForImageClassification, AutoImageProcessor
from PIL import Image
import torch

class ImageAnalyzer:
    def init(self, model_name=""):
        """test"""
        pass

    def analyze_images(self, analysed_dir, cats_dir, dogs_dir):
        """analysed results in cats or dogs"""
        pass

    def classify_image(self, image_path):
        """Classify a single image and return the predicted label and confidence."""
        pass

def init(self, model_name=""):
        """
        Initialize the analyzer with a pre-trained model from Hugging Face.

        Args:
            model_name (str): Name of the pre-trained model from Hugging Face.
        """
        self.model = AutoModelForImageClassification.from_pretrained(model_name)
        self.processor = AutoImageProcessor.from_pretrained(model_name)
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
        
def analyze_images(self, analysed_dir, cats_dir, dogs_dir):
        """
        Analyze all images in analysed_dir and move them to cats_dir or dogs_dir.

        Args:
            analysed_dir (str): Directory with analysed images.
            cats_dir (str): Directory to store cat images.
            dogs_dir (str): Directory to store dog images.

        Returns:
            list: List of dictionaries with classification results.
        """
        os.makedirs(cats_dir, exist_ok=True)
        os.makedirs(dogs_dir, exist_ok=True)

        results = []

        for filename in os.listdir(analysed_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(analysed_dir, filename)

                result = self.classify_image(image_path)
                result["filename"] = filename
                results.append(result)

                if result["error"] is None:
                    if "cat" in result["label"].lower():
                        shutil.move(image_path, os.path.join(cats_dir, filename))
                    elif "dog" in result["label"].lower():
                        shutil.move(image_path, os.path.join(dogs_dir, filename))
                    else:
                        result["error"] = f"Unexpected label: {result['label']}"

        return results
if name == "main": # type: ignore
    analyzer = ImageAnalyzer()
    results = analyzer.analyze_images(
        analysed_dir="data/analysed",
        cats_dir="data/cats",
        dogs_dir="data/dogs"
    )
    for result in results:
        print(result)