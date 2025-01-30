# ai-coloring-platform/generators/base_generator.py

import numpy as np
from PIL import Image, ImageDraw
import os
from datetime import datetime

class BaseGenerator:
    def __init__(self, output_dir="output/designs"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def create_blank_page(self, width=2480, height=3508):  # A4 at 300 DPI
        return Image.new('RGB', (width, height), 'white')

    def create_black_page(self, width=2480, height=3508):
        return Image.new('RGB', (width, height), 'black')

    def save_design(self, image, prefix="design"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}.png"
        path = os.path.join(self.output_dir, filename)
        image.save(path)
        return path

# ai-coloring-platform/generators/mandala_gen.py

from .base_generator import BaseGenerator
import math

class MandalaGenerator(BaseGenerator):
    def generate(self, complexity=8, size=2000):
        image = self.create_blank_page()
        draw = ImageDraw.Draw(image)

        center_x = image.width // 2
        center_y = image.height // 2
        max_radius = min(center_x, center_y) - 100

        # Generate mandala pattern
        for i in range(complexity):
            radius = max_radius * (i + 1) / complexity
            points = 8 * (i + 1)

            for j in range(points):
                angle = (2 * math.pi * j) / points
                x1 = center_x + radius * math.cos(angle)
                y1 = center_y + radius * math.sin(angle)

                # Draw connecting lines
                if j > 0:
                    draw.line([(prev_x, prev_y), (x1, y1)], fill='black', width=2)

                prev_x, prev_y = x1, y1

        return self.save_design(image, "mandala")

# Created/Modified files:
# - output/designs/mandala_{timestamp}.png