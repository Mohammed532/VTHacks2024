from PIL import Image, ImageDraw
import requests
import numpy as np
import torch
from transformers import DetrImageProcessor, DetrForObjectDetection
from PIL import ImageFilter
import replicate
import base64

file_name = 'object_mask.png'

image_url = "https://www.furniturestorelosangeles.com/media/catalog/product/cache/b9a5bb227f7b0b98d739db40c623248a/n/o/norwood-rustic-grey-bedroom-set.jpg"

# Load the image
def load_image(url):
    try: 
        return Image.open(requests.get(url, stream=True).raw)
    except Exception as e:
        print("There was an error loading your image")
        return None
    

def perform_detection(image):
    # Load object detection model and processor
    processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
    detection_model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")
    # Perform object detection
    inputs = processor(images=image, return_tensors="pt")
    outputs = detection_model(**inputs)
    target_sizes = torch.tensor([image.size[::-1]])
    results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.65)[0]  # Lowered threshold
    return results

def create_mask(image, results):
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
    mask.save("object_mask.png")  
    return mask
# Save the mask

def create_data_uri(file_path):
    with open(file_path, "rb") as file:
        # Read the file's contents
        file_data = file.read()
        # Encode the file data to base64
        encoded_data = base64.b64encode(file_data).decode('utf-8')
        # Construct the data URI
        data_uri = f"data:application/octet-stream;base64,{encoded_data}"
        return data_uri

def run_remover(mask_uri):
    output = replicate.run(
        "zylim0702/remove-object:0e3a841c913f597c1e4c321560aa69e2bc1f15c65f8c366caafc379240efd8ba",
        input={
            "mask": mask_uri, 
            "image": image_url
        }
    )
    print(output)

#optional debugging method 
def check_url_validity(url):
    response = requests.get(url)
    if response.status_code == 200:
        print("URL is accessible.")
    else:
        print(f"Failed to access URL. Status code: {response.status_code}")

def main(): 
    image = load_image(image_url) #through url 
    objects_detected = perform_detection(image)   
    create_mask(image, objects_detected) 
    mask_uri = create_data_uri("object_mask.png")
    run_remover(mask_uri)  # will pop out a url
    
if __name__ == "__main__":
    main()