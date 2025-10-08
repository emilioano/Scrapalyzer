from transformers import ViTImageProcessor, ViTForImageClassification
from PIL import Image
import requests

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = 'http://images.cocodataset.org/val2017/000000039769.jpg'
image = Image.open(requests.get(url, stream=True, verify=False).raw)

processor = ViTImageProcessor.from_pretrained('models/vit-base-patch16-224',local_files_only=True)
model = ViTForImageClassification.from_pretrained('models/vit-base-patch16-224',local_files_only=True)

inputs = processor(images=image, return_tensors="pt")
outputs = model(**inputs)
logits = outputs.logits
# model predicts one of the 1000 ImageNet classes
predicted_class_idx = logits.argmax(-1).item()
print("Predicted class:", model.config.id2label[predicted_class_idx])