from PIL import Image, ImageDraw
import random
import math
import os

# Get the path to the current directory
cwd = os.getcwd()

# Specify the relative path to the image file
image_path = os.path.join(cwd, "venv", "pngs", "flooney.png")

# Load the input image and convert it to RGBA mode
input_image = Image.open(image_path).convert("RGBA")

# Define the minimum and maximum cell sizes
min_cell_size = 220
max_cell_size = 240

# Define the buffer size around the edge of the output image
buffer_size = 20

# Calculate the size of the output image based on the grid cell size and buffer size
output_width = 14 * max_cell_size + buffer_size * 2
output_height = 14 * max_cell_size + buffer_size * 2

# Create a new image with an alpha channel and fill it with a gradient
output_image = Image.new("RGBA", (output_width, output_height), color=(255, 255, 255, 255))
draw = ImageDraw.Draw(output_image)

for x in range(output_width):
    for y in range(output_height):
        # Calculate the color of the pixel based on a diagonal gradient
        r = int(255 * x / output_width)
        g = int(255 * y / output_height)
        b = int(255 * (x + y) / (output_width + output_height))
        draw.point((x, y), fill=(r, g, b, 255))

# Calculate the random rotation angle and its sine and cosine values
angle = random.uniform(0, math.pi)
cos_angle = math.cos(angle)
sin_angle = math.sin(angle)

for x in range(14):
    for y in range(14):
        # Calculate the size of the grid cell
        cell_size = random.randint(min_cell_size, max_cell_size)

        # Calculate the coordinates of the top-left corner of the cell
        cell_x = x * max_cell_size + buffer_size
        cell_y = y * max_cell_size + buffer_size

        # Calculate the resize ratio based on two intersecting sine wave functions
        ratio = (math.sin((x / 14) * math.pi * 2 + (y / 14) * math.pi * 4) + math.sin((cos_angle * x / 14 + sin_angle * y / 14) * math.pi * 2)) * 0.2 + 0.8

        # Resize the input image using the Lanczos resampling filter
        resized_input_image = input_image.resize(
            (int(cell_size * ratio), int(cell_size * ratio)),
            resample=Image.LANCZOS,
        )

        # Convert the resized input image to RGBA mode
        resized_input_image = resized_input_image.convert("RGBA")

        # Calculate the center coordinates of the cell
        center_x = cell_x + max_cell_size // 2
        center_y = cell_y + max_cell_size // 2

        # Calculate the top-left coordinates of the resized input image
        resized_x = center_x - resized_input_image.width // 2
        resized_y = center_y - resized_input_image.height // 2

        # Paste the resized input image into the output image, preserving transparency
        output_image.alpha_composite(resized_input_image, (resized_x, resized_y))

# Save the output image
output_image.save("output_image.png")