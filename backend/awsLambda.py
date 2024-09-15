import json
import boto3
from PIL import Image, ImageDraw, ImageFilter
import requests
import torch
from transformers import DetrImageProcessor, DetrForObjectDetection
import replicate
import base64
import os

s3_client = boto3.client('s3')

def load_image_from_s3(bucket_name, file_key):
    # Download image from S3
    download_path = f'/tmp/{file_key}'
    s3_client.download_file(bucket_name, file_key, download_path)
    return Image.open(download_path)

def create_data_uri(file_path):
    with open(file_path, "rb") as file:
        file_data = file.read()
        encoded_data = base64.b64encode(file_data).decode('utf-8')
        data_uri = f"data:application/octet-stream;base64,{encoded_data}"
        return data_uri

def run_remover(mask_uri, image_url):
    output = replicate.run(
        "zylim0702/remove-object:0e3a841c913f597c1e4c321560aa69e2bc1f15c65f8c366caafc379240efd8ba",
        input={
            "mask": mask_uri, 
            "image": image_url
        }
    )
    return output

def lambda_handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']

    # Load the image from S3
    image = load_image_from_s3(bucket_name, file_key)
    
    # Object detection
    processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
    detection_model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")
    
    inputs = processor(images=image, return_tensors="pt")
    outputs = detection_model(**inputs)
    
    target_sizes = torch.tensor([image.size[::-1]])
    results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.65)[0]
    
    # Create the mask
    mask = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(mask)
    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        box = [int(i) for i in box]
        draw.rectangle(box, outline=255, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=2))
    
    mask_path = "/tmp/object_mask.png"
    mask.save(mask_path)
    
    # Generate data URI for the mask
    mask_uri = create_data_uri(mask_path)
    
    #WE MIGHT NEED TO CREATE_DATA_URI(IMAGE_PATH)


    # Run the object removal
    result = run_remover(mask_uri, f"s3://{bucket_name}/{file_key}")
    
    # Save the processed result back to S3 (optional)
    output_key = f"processed/{file_key}"
    s3_client.put_object(Bucket=bucket_name, Key=output_key, Body=result)

    return {
        'statusCode': 200,
        'body': json.dumps('Object processed and saved to S3.')
    }