from flask import Flask, request, render_template, send_from_directory
import os
from PIL import Image, ImageDraw
import numpy as np
import uuid  # Import the uuid module to generate unique filenames

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['CROPS_FOLDER'] = 'crops'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['CROPS_FOLDER']):
    os.makedirs(app.config['CROPS_FOLDER'])

from PIL import ImageFilter



def color_difference(color1, color2):
    # Calculate the color tone difference between two colors
    r1, g1, b1, a1 = color1
    r2, g2, b2, a2 = color2
    tone_difference = abs(r1 - r2) + abs(g1 - g2) + abs(b1 - b2)
    return tone_difference

# def crop_image(image_path, polygons):
#     cropped_images = []

#     for i, polygon in enumerate(polygons):
#         # Open the image using Image.open
#         img = Image.open(image_path)

#         # Create a blank image with a transparent background
#         cropped_img = Image.new('RGBA', (img.width, img.height), (0, 0, 0, 0))

#         # Create a drawing context for the polygon mask
#         draw = ImageDraw.Draw(cropped_img)

#         # Draw the polygon on the new image to create the mask
#         draw.polygon(polygon, outline=(0, 0, 0, 255), fill=(0, 0, 0, 255))

#         # Paste the content of the polygon from the original image onto the transparent background
#         cropped_img.paste(img, (0, 0), mask=cropped_img)

#         # Define a threshold for color tone difference from black
#         tone_threshold = 350

#         # Remove colors that are not within the threshold of black
#         for x in range(cropped_img.width):
#             for y in range(cropped_img.height):
#                 pixel = cropped_img.getpixel((x, y))
#                 if color_difference(pixel, (0, 0, 0, 255)) > tone_threshold:
#                     cropped_img.putpixel((x, y), (0, 0, 0, 0))

#         # Save the cropped image with a unique filename in PNG format
#         crop_path = os.path.join(app.config['CROPS_FOLDER'], f'crop_{i}.png')
#         cropped_img.save(crop_path, format='PNG')
#         cropped_images.append(cropped_img)

#     return cropped_images



def crop_image(image_path, polygons):
    cropped_images = []

    for i, polygon in enumerate(polygons):
        # Open the image using Image.open
        img = Image.open(image_path)

        # Create a blank image with a transparent background
        cropped_img = Image.new('RGBA', (img.width, img.height), (0, 0, 0, 0))

        # Create a drawing context for the polygon mask
        draw = ImageDraw.Draw(cropped_img)

        # Draw the polygon on the new image to create the mask
        draw.polygon(polygon, outline=(0, 0, 0, 255), fill=(0, 0, 0, 255))

        # Paste the content of the polygon from the original image onto the transparent background
        cropped_img.paste(img, (0, 0), mask=cropped_img)

        # Define a threshold for color tone difference from black
        tone_threshold = 355

        # Remove colors that are not within the threshold of black
        for x in range(cropped_img.width):
            for y in range(cropped_img.height):
                pixel = cropped_img.getpixel((x, y))
                if color_difference(pixel, (0, 0, 0, 255)) > tone_threshold:
                    cropped_img.putpixel((x, y), (0, 0, 0, 0))

        # Apply Gaussian blur to the alpha channel (transparency) to smooth the outer edge
        alpha = cropped_img.split()[3]  # Extract the alpha channel
        alpha = alpha.filter(ImageFilter.GaussianBlur(radius=0.5))  # Apply Gaussian blur
        cropped_img.putalpha(alpha)  # Update the alpha channel with the blurred version

        # Save the cropped image with a unique filename in PNG format
        crop_path = os.path.join(app.config['CROPS_FOLDER'], f'crop_{i}.png')
        cropped_img.save(crop_path, format='PNG')
        cropped_images.append(cropped_img)

    return cropped_images









@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Define hardcoded polygon coordinates for cropping
        polygons = [
            [(45, 45), (298, 45), (298, 217), (127, 217), (127, 141), (45, 140)],  # Polygon 1
            [(298, 45), (488, 45), (488, 87), (298, 91)],  # Polygon 2
            [(298, 87), (488, 87), (488, 45), (596, 45), (596, 239), (298, 238)],  # Polygon 3
            [(596, 45), (1013, 45), (1013, 330), (789, 330), (789, 414), (720, 414), (720, 238), (596, 239)],
            [(1013, 45), (1248, 45), (1248, 160), (1156, 160), (1156, 239), (1013, 242)],
            [(1156, 160), (1248, 160), (1248, 239), (1156, 239)],
            [(1248, 45), (1337, 45), (1337, 105), (1425, 105), (1425, 375), (1248, 375)],
            [(1337, 45), (1481, 45), (1481, 105), (1337, 105)],
            [(1425, 105), (1463, 105), (1463, 375), (1425, 375)],
            [(1483, 45), (1635, 45), (1635, 690), (1463, 690), (1463, 105), (1481, 105)]
            # Add more polygons as needed
        ]


        # Perform cropping based on predefined polygons
        cropped_images = crop_image(file_path, polygons)

        # No collage creation; each crop is saved as a separate image

        return "Crops saved as separate images."

if __name__ == '__main__':
    app.run(debug=True)
