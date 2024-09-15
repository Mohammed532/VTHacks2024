from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image, ImageDraw, ImageFilter
import torch
from transformers import DetrImageProcessor, DetrForObjectDetection
import replicate
import base64
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def load_image(file):
    try:
        return Image.open(file)
    except Exception as e:
        print("There was an error loading your image")
        return None

def perform_detection(image):
    processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
    detection_model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")
    inputs = processor(images=image, return_tensors="pt")
    outputs = detection_model(**inputs)
    target_sizes = torch.tensor([image.size[::-1]])
    results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.65)[0]
    return results

def create_mask(image, results):
    mask = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(mask)
    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        box = [int(i) for i in box]
        print(f"Drawing box with coordinates: {box}")
        draw.rectangle(box, outline=255, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=2))
    mask_path = os.path.join(UPLOAD_FOLDER, "object_mask.png")
    mask.save(mask_path)
    return mask_path

def create_data_uri(file_path):
    with open(file_path, "rb") as file:
        file_data = file.read()
        encoded_data = base64.b64encode(file_data).decode('utf-8')
        data_uri = f"data:application/octet-stream;base64,{encoded_data}"
        return data_uri

def run_remover(mask_uri, image_file):
    client = replicate.Client('zylim0702/remove-object:0e3a841c913f597c1e4c321560aa69e2bc1f15c65f8c366caafc379240efd8ba')
    output = client.run(
        "zylim0702/remove-object:0e3a841c913f597c1e4c321560aa69e2bc1f15c65f8c366caafc379240efd8ba",
        input={
            "mask": mask_uri, 
            "image": image_file
        }
    )
    return output

@app.route('/upload', methods=['POST'])
def upload_images():
    if 'files' not in request.files:
        return jsonify({"error": "No files part"}), 400
    
    files = request.files.getlist('files')
    if not files:
        return jsonify({"error": "No selected files"}), 400

    result_urls = {}
    
    for file in files:
        if file.filename == '':
            continue
        
        image_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(image_path)
        
        image = load_image(image_path)
        if image is None:
            continue
        
        objects_detected = perform_detection(image)
        mask_path = create_mask(image, objects_detected)
        mask_uri = create_data_uri(mask_path)
        
        output_url = run_remover(mask_uri, image_path)
        result_urls[file.filename] = output_url

    print(result_urls) 
    return jsonify(result_urls)

if __name__ == '__main__':
    app.run(debug=True)
