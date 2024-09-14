from io import BytesIO
import torch
from transformers import DetrImageProcessor, DetrForObjectDetection
from diffusers import StableDiffusionInpaintPipeline
from PIL import Image, ImageDraw
import requests
import numpy as np

urlImage = "https://www.reidsfurnishings.com/wp-content/uploads/2022/10/hero-bath.jpg"

# Load object detection model and processor
detection_model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")
processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")

# Load the inpainting model
inpainting_model = StableDiffusionInpaintPipeline.from_pretrained("stabilityai/stable-diffusion-2-inpainting")

#Open up image
response = requests.get(urlImage)
image = Image.open(BytesIO(response.content)).convert("RGB")

#Perform the actual object detection
inputs = processor(images=image, return_tensors="pt")
outputs = detection_model(**inputs)

target_sizes = torch.tensor([image.size[::-1]])
results = processor.post_process_object_detection(outputs, target_sizes=target_sizes)[0]

mask = Image.new("L", image.size, 0)  # Black mask with the same size as the image
draw = ImageDraw.Draw(mask)

for box in results["boxes"]:
    draw.rectangle(box.tolist(), outline=255, fill=255)

# Perform inpainting
result = inpainting_model(prompt="A clean room without furniture", init_image=image, mask_image=mask).images[0]

# Save or display the result
result.save("cleaned_room.png")
result.show()