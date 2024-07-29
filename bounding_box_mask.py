# Author: adityaa-chandna
# Date: 29th July, 2024

# Program to convert CSV files containing bounding boxes into a PNG file
# The PNG file is a solid black image with white pixels denoting the area covered by a bounding box
# Adjust the image_path and csv_path parameters as needed
# Name the output file as needed


import pandas as pd
from PIL import Image

def create_image_from_csv(csv_file, output_image_file, width, height):
    # Read the CSV file into a DataFrame, using only the relevant columns
    df = pd.read_csv(csv_file, usecols=['xmin', 'ymin', 'xmax', 'ymax'])
    
    # Create a black image
    image = Image.new('RGB', (width, height), color='black')
    pixels = image.load()
    
    # Iterate through each row in the DataFrame
    for _, row in df.iterrows():
        xmin, ymin, xmax, ymax = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
        
        # Ensure coordinates are within the image dimensions
        xmin = max(0, xmin)
        xmax = min(width - 1, xmax)
        ymin = max(0, ymin)
        ymax = min(height - 1, ymax)
        
        # Draw white pixels within the bounding box
        for x in range(xmin, xmax + 1):
            for y in range(ymin, ymax + 1):
                pixels[x, y] = (255, 255, 255)
    
    # Save the image
    image.save(output_image_file)

def get_image_dimensions(image_path):
    # Open the image file
    with Image.open(image_path) as img:
        # Get image dimensions
        width, height = img.size
        return width, height

# Specify the path to your image
image_path = 'sampleQLDimageXX.png'
csv_path = 'sampleQLDcsvXX.csv'

# Get and print the image dimensions
width, height = get_image_dimensions(image_path)

# Hardcoded image width and height
# Define the image dimensions
# width, height = 458, 196

# Call the function with your CSV file and desired output image file name
create_image_from_csv(csv_path, 'boxmaskXX.png', width, height)
