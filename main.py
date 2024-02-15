import os
import cv2
import numpy as np
from photomosaic import photomosaic
import enhancements

canvas_path = './images/mario.bmp'
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
# for testing result
# binilnear = cv2.resize(canvas, (320, 320), interpolation = cv2.INTER_LINEAR)
# answer = cv2.resize(canvas, (320, 320), interpolation = cv2.INTER_CUBIC)
synthesisCubic = enhancements.photomosaic_Cubic(canvas, tiles, W, H, w, h)
synthesisDithering = enhancements.photomosaic_dithering_bilinear(canvas, tiles, W, H, w, h, 8)
ditheringOnly = enhancements.ditheringOnly(canvas, 8)
# cv2.imwrite('synthesisCV2.png', np.array(answer).astype(np.uint8))
# cv2.imwrite('synthesisCV2_binilear.png', np.array(binilnear).astype(np.uint8))

cv2.imwrite('synthesis.png', np.array(synthesis).astype(np.uint8))
cv2.imwrite('ditheringOnly.png', np.array(ditheringOnly).astype(np.uint8))
cv2.imwrite('synthesisDithering.png', np.array(synthesisDithering).astype(np.uint8))
cv2.imwrite('synthesisCubic.png', np.array(synthesisCubic).astype(np.uint8))


