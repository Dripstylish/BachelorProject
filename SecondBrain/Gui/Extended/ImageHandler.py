import numpy as np
from PIL import Image, ImageDraw


class Icon:
    def __init__(self, image, width=None, height=None):
        self.image = image

    def create_round_image(self, name):
        # Open the input image as numpy array, convert to RGB
        img = Image.open(self.image).convert("RGB")
        npImage = np.array(img)
        h, w = img.size

        # Create same size alpha layer with circle
        alpha = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(alpha)
        draw.pieslice([0, 0, h, w], 0, 360, fill=255)

        # Convert alpha Image to numpy array
        npAlpha = np.array(alpha)

        # Add alpha layer to RGB
        npImage = np.dstack((npImage, npAlpha))

        # Save with alpha
        Image.fromarray(npImage).save(name)

        return name
