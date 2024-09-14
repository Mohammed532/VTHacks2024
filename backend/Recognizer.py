from io import BytesIO
import torch
from transformers import DetrImageProcessor, DetrForObjectDetection
from diffusers import StableDiffusionInpaintPipeline
from PIL import Image, ImageDraw
import requests
import numpy as np

url = "https://i5.walmartimages.com/seo/HONBAY-Upholstered-Convertible-Sectional-Sofa-Couch-with-Storage-for-Living-Room-Furniture-Sets-Green_bcfc7256-6f27-4dfd-b9ed-99a4c8930560.e5de50114252156264cd0e35030455b1.jpeg"
image = Image.open(requests.get(url, stream=True).raw)

# Load object detection model and processor
processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
detection_model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")

# #Open up image
# response = requests.get(urlImage)

#Perform the actual object detection
inputs = processor(images=image, return_tensors="pt")
outputs = detection_model(**inputs)

target_sizes = torch.tensor([image.size[::-1]])
results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.85)[0] #only keep objects with a 75%

for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
    box = [round(i, 2) for i in box.tolist()]
    print(
            f"Detected {detection_model.config.id2label[label.item()]} with confidence "
            f"{round(score.item(), 3)} at location {box}"
    )