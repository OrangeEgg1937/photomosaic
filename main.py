import os
import cv2
import numpy as np
from photomosaic import photomosaic
import enhancements

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

# For enhancement features
# binilnear = cv2.resize(canvas, (320, 320), interpolation = cv2.INTER_LINEAR)
# answer = cv2.resize(canvas, (320, 320), interpolation = cv2.INTER_CUBIC)
result = enhancements.photomosaic_Cubic(canvas, tiles, W, H, w, h)

cv2.imwrite('synthesis.png', np.array(synthesis).astype(np.uint8))
cv2.imwrite('synthesis_enh_cubic.png', np.array(result).astype(np.uint8))
# cv2.imwrite('synthesisCV2.png', np.array(answer).astype(np.uint8))

