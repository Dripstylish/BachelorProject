import numpy as np
from PIL import Image, ImageDraw


class Icon:
    def __init__(self, image):
        self.image = image

    def create_round_image(self, name):
        img = Image.open(self.image).convert("RGB")
        npImage = np.array(img)
        h, w = img.size
        alpha = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(alpha)
        draw.pieslice([0, 0, h, w], 0, 360, fill=255)
        npAlpha = np.array(alpha)
        npImage = np.dstack((npImage, npAlpha))
        Image.fromarray(npImage).save(name)

        return name