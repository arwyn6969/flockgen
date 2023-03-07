from PIL import Image
import random
import math
import os

# Get the path to the current directory
cwd = os.getcwd()

# Specify the relative path to the image file
input_image = Image.open("pngs/flooney.png").convert("RGBA")


# Load the input image and convert it to RGBA mode
input_image = Image.open(image_path).convert("RGBA")

# Calculate the size of each grid cell based on the input image size
cell_width = 200
cell_height = 200

# Calculate the size of the output image based on the grid cell size
output_width = 12 * cell_width
output_height = 12 * cell_height

# Create a new image with an alpha channel
output_image = Image.new("RGBA", (output_width, output_height), color=(0, 0, 0, 0))

angle = random.uniform(0, math.pi)
cos_angle = math.cos(angle)
sin_angle = math.sin(angle)

for x in range(12):
    for y in range(12):
        # Calculate the coordinates of the top-left corner of the cell
        cell_x = x * cell_width
        cell_y = y * cell_height

        # Calculate the resize ratio based on two intersecting sine wave functions
        ratio = (math.sin((x / 12) * math.pi * 2 + (y / 12) * math.pi * 4) + math.sin((cos_angle * x / 12 + sin_angle * y / 12) * math.pi * 2)) * 0.2 + 0.8


        # Resize the input image using the Lanczos resampling filter
        resized_input_image = input_image.resize(
            (int(cell_width * ratio), int(cell_height * ratio)),
            resample=Image.LANCZOS,
        )

        # Convert the resized input image to RGBA mode
        resized_input_image = resized_input_image.convert("RGBA")

        # Calculate the center coordinates of the cell
        center_x = cell_x + cell_width // 2
        center_y = cell_y + cell_height // 2

        # Calculate the top-left coordinates of the resized input image
        resized_x = center_x - resized_input_image.width // 2
        resized_y = center_y - resized_input_image.height // 2

        # Paste the resized input image into the output image, preserving transparency
        output_image.alpha_composite(resized_input_image, (resized_x, resized_y))

# Save the output image
output_image.save("output_image.png")
