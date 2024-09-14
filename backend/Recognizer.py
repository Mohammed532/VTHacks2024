from PIL import Image, ImageDraw
import requests
import numpy as np
import torch
from transformers import DetrImageProcessor, DetrForObjectDetection

# Load the image
url = "https://www.alhabibpaneldoors.com/images/interior-item/modern-lcd-cabinet-wall-shelves-furniture-design-ipc511.jpeg"
image = Image.open(requests.get(url, stream=True).raw)

# Load object detection model and processor
processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
detection_model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")

# Perform object detection
inputs = processor(images=image, return_tensors="pt")
outputs = detection_model(**inputs)
target_sizes = torch.tensor([image.size[::-1]])
results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.86)[0]

# Create the mask
mask = Image.new('L', image.size, 0)  # 'L' mode for grayscale
draw = ImageDraw.Draw(mask)

# Draw bounding boxes on the mask
for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
    box = [int(i) for i in box]
    print(f"Drawing box with coordinates: {box}")  # Debugging print
    draw.rectangle(box, outline=255, fill=255)  # Draw white rectangles

mask.show()  # Show the mask to verify

# Save the mask
mask.save("object_mask.png")
