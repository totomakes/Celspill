from flask import request
from app import app
import os
from PIL import Image

@app.route('/upload', methods=['POST'])
def upload():
    # ... (previous code)

    # Define hardcoded polygon coordinates
    polygons = [
        [(45, 45), (298, 45), (298, 217), (127, 217), (125, 387), (45, 387)],  # Polygon 1
        [(298, 45), (488, 45), (488, 87), (298, 91)],  # Polygon 2
        [(298, 87), (488, 87), (488, 45), (596, 45), (596, 239), (298, 238)]  # Polygon 3
        # Add more polygons as needed
    ]


    # Perform cropping based on custom polygons
    cropped_images = crop_image(file_path, polygons)
    collage = create_collage(cropped_images, len(polygons))

    # Save and display the collage
    collage_path = os.path.join(app.config['COLLAGE_FOLDER'], 'collage.jpg')
    collage.save(collage_path)
    return send_from_directory(app.config['COLLAGE_FOLDER'], 'collage.jpg')
