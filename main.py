import os
import cv2
from cv2.gapi import RGB2Gray
import numpy as np
from numpy.compat import integer_types
from photomosaic import photomosaic


canvas_path = './images/cat.bmp'
tile_dir = './tiles'
W = H = 320
w = h = 10

canvas = cv2.imread(canvas_path).astype(float)
tiles = []
for tile_file in os.listdir(tile_dir):
    tile_path = os.path.join(tile_dir, tile_file)
    tiles.append(cv2.imread(tile_path).astype(float))

# implement the function `photomosaic`
synthesis = photomosaic(canvas, tiles, W, H, w, h)
cv2.imwrite('synthesis.png', np.array(synthesis).astype(np.uint8))
