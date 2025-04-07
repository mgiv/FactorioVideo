import os
from PIL import Image
import numpy as np
import json

def get_images():
    images = []

    dir = os.fsencode("vid")

    for file in os.listdir(dir):
        filename = os.fsdecode(file)
        img = Image.open("vid/" + filename).convert('RGB')
        pixels = img.load()
        width, height = img.size

        image_int = []

        for x in range(width):
            row = []
            for y in range(height):
                r, g, b = pixels[x, y]

                hex_int = (r << 16) + (g << 8) + b
                row.append(hex_int)
            image_int.append(row)
        images.append(image_int)
    return images

def convert_images():
    images = get_images()
    open("output.txt", "w").write(str(images))

    arr = np.array(images[0], dtype=np.uint32)
    blue = (arr & 0xFF).astype(np.uint8)
    green = ((arr >> 8) & 0xFF).astype(np.uint8)
    red = ((arr >> 16) & 0xFF).astype(np.uint8)

    height, width = 160, 90  # Replace with actual dimensions
    rgb_array = np.stack([red, green, blue], axis=-1).reshape((height, width, 3))

    return rgb_array