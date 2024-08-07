import csv
import os
import requests
import cv2
from datetime import datetime
import argparse

# Author - Rajesh Roy (rajeshroy402@gmail.com)

# Function to download images
def download_image(image_url, save_path):
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # Check if the request was successful
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {image_url}: {e}")

# Function to add text to an image using OpenCV
def add_text_to_image(image_path, text):
    try:
        image = cv2.imread(image_path)
        
        # Define the font and size
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 2
        font_color = (255, 0, 255)  # Pink color in BGR
        font_thickness = 3
        
        # Calculate the position for the text (top right corner)
        text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
        position = (image.shape[1] - text_size[0] - 10, text_size[1] + 10)  # 10 pixels padding from the edge
        
        # Add text to the image
        cv2.putText(image, text, position, font, font_scale, font_color, font_thickness)
        
        # Save the modified image
        cv2.imwrite(image_path, image)
        print(f"Added text to: {image_path}")
    except Exception as e:
        print(f"Error adding text to {image_path}: {e}")

# Main function to process the CSV file and download images
def main(csv_file_path):
    # Directory to save images
    images_dir = 'downloaded_images'
    os.makedirs(images_dir, exist_ok=True)
    
    # Get the current system time and format it
    current_time = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Read the CSV file and download images
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            image_url = row['image']
            outlet_number = row['outlet']
            image_id = row['id']
            created_at = row['tat']
            
            # Create directory for the outlet with current time if it doesn't exist
            outlet_dir = os.path.join(images_dir, f"{outlet_number}_{current_time}")
            os.makedirs(outlet_dir, exist_ok=True)
            
            # Define the save path for the image
            save_path = os.path.join(outlet_dir, f"{image_id}.jpg")
            
            # Download the image
            download_image(image_url, save_path)
            
            # Add the created_at text to the image
            add_text_to_image(save_path, created_at)

    print("Image download and annotation process completed.")

# Parse command line arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download and annotate images from a CSV file.')
    parser.add_argument('csv_file', help='Path to the CSV file')
    args = parser.parse_args()
    
    main(args.csv_file)

