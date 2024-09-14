from PIL import Image, ImageDraw
import requests
import numpy as np
import torch
from transformers import DetrImageProcessor, DetrForObjectDetection
from PIL import ImageFilter

import replicate


# Load the image
url = "https://www.furniturestorelosangeles.com/media/catalog/product/cache/b9a5bb227f7b0b98d739db40c623248a/n/o/norwood-rustic-grey-bedroom-set.jpg"
image = Image.open(requests.get(url, stream=True).raw)

# Load object detection model and processor
processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
detection_model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")

# Perform object detection
inputs = processor(images=image, return_tensors="pt")
outputs = detection_model(**inputs)
target_sizes = torch.tensor([image.size[::-1]])
results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.70)[0]  # Lowered threshold

# Create the mask
mask = Image.new('L', image.size, 0)  # 'L' mode for grayscale
draw = ImageDraw.Draw(mask)

# Draw bounding boxes on the mask
for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
    box = [int(i) for i in box]
    print(f"Drawing box with coordinates: {box}")  # Debugging print
    draw.rectangle(box, outline=255, fill=255)  # Draw white rectangles

mask = mask.filter(ImageFilter.GaussianBlur(radius=2))
mask.show()  # Show the mask to verify

# Save the mask
mask.save("object_mask.png")  #THIS IMAGE NEEDS TO BE SAVED IN S3 BUCKET

output = replicate.run(
    "zylim0702/remove-object:0e3a841c913f597c1e4c321560aa69e2bc1f15c65f8c366caafc379240efd8ba",
    input={
        "mask": "object_mask.png", 
        "image": url
    }
)

output.show()
output.show("finalize_output.png")