# implementation of the function `photomosaic`
# you are not allowed to use any third-party libraries
# import timeit # for program runtime testing

# class for storing the gray image and its brightness
class GrayImage:  
    def __init__(self, image, brightness):
        self.image = image
        self.brightness = brightness

# self-define function for math operation
def max(a, b):
    if a > b:
        return a
    else:
        return b
    
def min(a, b):
    if a < b:
        return a
    else:
        return b

def ceil(a):
    if a - int(a) > 0:
        return int(a) + 1
    else:
        return int(a)

def floor(a):
    return int(a)

# replicate padding for the image
def replicate_padding(image):
    # get the original width and height
    h = len(image)
    w = len(image[0])
    
    # create a new image array
    padded_image = []
    
    # replicate padding
    for i in range(h + 4):
        temp = []
        for j in range(w + 4):
            # replicate padding
            if i < 2: # top
                y = 0
            elif i >= h + 2: # bottom
                y = h - 1
            else:
                y = i - 2 # middle (copying the original img)
                
            if j < 2: # left
                x = 0
            elif j >= w + 2: # right
                x = w - 1
            else:
                x = j - 2 # middle (copying the original img)
            
            temp.append(image[y][x]) # copy the pixel value
        padded_image.append(temp) # append the new row to the result
        
    return padded_image

# bicubic kernel equation
def cubic_kernel(distance, a:float):
    distance = abs(distance)
    if distance <= 1:
        return (a + 2) * (distance ** 3) - (a + 3) * (distance ** 2) + 1
    elif distance < 2:
        return a * (distance ** 3) - 5 * a * (distance ** 2) + 8 * a * distance - 4 * a
    else:
        return 0

# bilinear interpolation for resizing the image from giving width and height
def cubic_interpolation(image, width, hight):
    # get the original width and height
    original_h = len(image)
    original_w = len(image[0])
    
    # get the ratio of the original image and the target image
    width_ratio = original_w / (width)
    hight_ratio = original_h / (hight)

    # create a new image array
    result = []
    
    # padding the image
    image = replicate_padding(image)
    
    # bicubic interpolation part
    #     dx
    #   |---------|
    #   |--||-------------------------|
    # dy|  ||p0    p1     p2     p3   | y0
    #   |  ||p4    p5     p6     p7   | y1
    #   |--||         R(x, y)         |
    #      |p8    p9     p10    p11   | y2
    #      |p12   p13    p14    p15   | y3
    #      |------------------------- |
    #        x0       x1     x2     x3
    for h in range(hight):
        temp = []
        for w in range(width):
            # map the output coordinates to the mapped image
            x = (w + 0.5) * width_ratio + 1.5
            y = (h + 0.5) * hight_ratio + 1.5
            
            # get the x and y coordinate of the 16 points
            dx = []
            dx.append(int(x - 1))
            dx.append(int(x))
            dx.append(int(x + 1))
            dx.append(int(x + 2))
            
            dy = []
            dy.append(int(y - 1))
            dy.append(int(y))
            dy.append(int(y + 1))
            dy.append(int(y + 2))
            
            # find the weight of the 16 points
            w = []
            for i in range(4):
                for j in range(4):
                    w.append(cubic_kernel(x - dx[i], -0.75) * cubic_kernel(y - dy[j], -0.75))
            
            # calculate the pixel value
            final_pixel = 0.0
            for i in range(4):
                for j in range(4):
                    final_pixel += w[i * 4 + j] * image[dy[j]][dx[i]]
                    
            # append the result to the new image
            temp.append(final_pixel)
        result.append(temp)
    
        
    return result

# bilinear interpolation for resizing the image from giving width and height
def bilinear_interpolation(image, width, hight):
    # get the original width and height
    original_h = len(image)
    original_w = len(image[0])
    
    # get the ratio of the original image and the target image
    width_ratio = original_w / (width)
    hight_ratio = original_h / (hight)

    # create a new image array
    result = []

    # bilinear interpolation part
    # (x1, y1)            (x2, y1)
    #    p0------------------p1
    #    |     .R(x, y)       |
    #    |                    |  
    #    p2------------------p3
    # (x1, y2)            (x2, y2)
    for i in range(hight):
        temp = []
        for j in range(width):
            # find the floor and ceil value of the x and y
            # if the value is out of the range (x < 0 or x > w), set it to the max/min value
            # here will be use nearest neighbor interpolation
            x_lower = max(min(floor(j * width_ratio), original_w - 1), 0)
            x_upper = max(min(ceil(j * width_ratio), original_w - 1), 0)
            y_lower = max(min(floor(i * hight_ratio), original_h - 1), 0)
            y_upper = max(min(ceil(i * hight_ratio), original_h - 1), 0)

            # get the value of the four points
            p0 = image[y_lower][x_lower]
            p1 = image[y_lower][x_upper]
            p2 = image[y_upper][x_lower]
            p3 = image[y_upper][x_upper]
            
            # calculate the total area for weighted mean later on
            total_area = (x_upper - x_lower) * (y_upper - y_lower)
            
            # checking the total area
            # if the total area is 0, there must be a point on the edge/it is a single point
            # here will be use nearest neighbor interpolation or interpolate a line
            if (total_area == 0):
                # checking the x-axis
                if (x_lower - x_upper == 0 and y_lower - y_upper != 0):
                   # set the weight to 0 for p1 and p3
                   w0 = (y_upper - i * hight_ratio) / (y_upper - y_lower)
                   w1 = 0
                   w2 = (i * hight_ratio - y_lower) / (y_upper - y_lower)
                   w3 = 0
                # checking the y-axis
                elif (x_lower - x_upper != 0 and y_lower - y_upper == 0):
                   # set the weight to 0 for p2 and p3
                   w0 = (x_upper - j * width_ratio) / (x_upper - x_lower)
                   w1 = (j * width_ratio - x_lower) / (x_upper - x_lower)
                   w2 = 0
                   w3 = 0
                else: # it is a single point, so it means p0 = p1 = p2 = p3
                   # set the weight to 1 for p0 as we only take it
                   w0 = 1
                   w1 = 0
                   w2 = 0
                   w3 = 0
            else: # normal case
                w0 = (x_upper - j * width_ratio) * (y_upper - i * hight_ratio) / total_area
                w1 = (j * width_ratio - x_lower) * (y_upper - i * hight_ratio) / total_area
                w2 = (x_upper - j * width_ratio) * (i * hight_ratio - y_lower) / total_area
                w3 = (j * width_ratio - x_lower) * (i * hight_ratio - y_lower) / total_area
            
            # calculate the new pixel value
            new_pixel = w0 * p0 + w1 * p1 + w2 * p2 + w3 * p3
            
            # append the new pixel value to the result
            temp.append(new_pixel)
            
        # append the new row to the result
        result.append(temp)
        
    return result

# For image, convert RGB to brightness and find average brightness process
def image2brightness(canvas, width, hight) -> GrayImage:
    # get the size of the tile
    sizeOfTile = width * hight
    
    # total number of tiles
    totalNumberOfTile = (len(canvas) * len(canvas[0])) / sizeOfTile
    
    # create an array to store the brightness of each tile
    brightness = [0.0] * int(totalNumberOfTile)
    
    # number of tiles in a row
    numOfTileInRow = int(len(canvas[0]) / width)

    # convert the canvas color to gary
    result = []
    for y in range(len(canvas)):
        temp = []
        for x in range(len(canvas[y])):
            # convert the RGB to brightness
            pixel = 0.299 * canvas[y][x][0] + 0.587 * canvas[y][x][1] + 0.114 * canvas[y][x][2]
            temp.append(pixel)
            
            # calculate the tile number
            tileNumber = int(y / hight) * numOfTileInRow + int(x / width)
            
            # add the brightness to the tile
            brightness[tileNumber] += pixel
        result.append(temp)
        
    # calculate the average brightness
    for i in range(len(brightness)):
        brightness[i] = brightness[i] / sizeOfTile
    
    # in image, the brightness is the average brightness of the canvas for each tile, not each pixel
    return GrayImage(result, brightness)
 
# For each tile, convert RGB to brightness and find average brightness process
def tile2brightness(tiles) -> GrayImage:
    # convert the canvas color to gary
    result = []
    total_value = 0.0
    for pixel in tiles:
        temp = []
        for i in range(len(pixel)):
            temp.append(0.299 * pixel[i][0] + 0.587 * pixel[i][1] + 0.114 * pixel[i][2])
            total_value += temp[i]
        result.append(temp)
        
    # calculate the average brightness
    average_brightness = total_value / (len(tiles) * len(tiles[0]))
    
    return GrayImage(result, average_brightness)

# creating a Bayer matrix for dithering
def BayerMatrix(n):
    # define the base case 2x2 matrix
    base = [[0, 2], 
            [3, 1]]
    
    while n > 2:
        # create a new matrix with 4 times the size of the original matrix
        new_base = []
        for i in range(2 * len(base)):
            temp = []
            for j in range(2 * len(base)):
                temp.append(0)
            new_base.append(temp)
        
        # copy the original matrix to the new matrix
        for i in range(len(base)):
            for j in range(len(base)):
                new_base[i][j] = 4 * base[i][j]
                new_base[i][j + len(base)] = 4 * base[i][j] + 2
                new_base[i + len(base)][j] = 4 * base[i][j] + 3
                new_base[i + len(base)][j + len(base)] = 4 * base[i][j] + 1
        
        # update the base matrix
        base = new_base
        n = n / 2
    
    return base

# Dithering process
def Dithering(canvas:GrayImage, bayerSize):
    # get the original width and height
    h = len(canvas.image)
    w = len(canvas.image[0])
    
    # create a new image array
    result = []
    
    # create a Bayer matrix for dithering
    bayer = BayerMatrix(bayerSize)
    
    # dithering process
    for y in range(h):
        temp = []
        for x in range(w):
            # get the pixel value
            pixel = canvas.image[y][x]
            
            # get the threshold value
            threshold = bayer[y % bayerSize][x % bayerSize]
            
            # compare the pixel value with the threshold value
            if pixel > threshold:
                temp.append(255)
            else:
                temp.append(0)
        result.append(temp)
        
    return result


# To find the nearest brightness tile for each tile
def FindNearestTiles(brightness, tilePool):
    # early leave for the edge case
    if brightness >= tilePool[-1].brightness:
        return tilePool[-1].image
    elif brightness <= tilePool[0].brightness:
        return tilePool[0].image
    
    # set the initial value for the binary search
    left = 0
    right = len(tilePool) - 1
    
    # binary search
    while left < right:
        mid = int((left + right) / 2)

        # if the brightness of the tile is less than the target brightness, move the left pointer to the right
        if tilePool[mid].brightness < brightness:
            left = mid + 1
        elif tilePool[mid].brightness > brightness:
            right = mid - 1
        elif tilePool[mid].brightness == brightness: # if found excetly the same brightness, return the image
            return tilePool[left].image
    
    # Verify the result
    # For example, if the pool like {1, 3, 4, 5}, key = 3.1, the current left pointer is 2
    # however, it should be 1, so we need to check the left pointer and the left pointer - 1
    # to find the nearest brightness tile
    if tilePool[left].brightness - brightness < brightness - tilePool[left - 1].brightness:
        return tilePool[left].image
    else:
        return tilePool[left-1].image

# Compose the tiles to the canvas
def ComposeTiles(canvas:GrayImage, tiles, width, hight):
    # get the number of tiles in a row and a column
    numberOfTileInRow = int(len(canvas.image[0]) / width)
    numberOfTileInCol = int(len(canvas.image) / hight)
    
    # for every tile, find the nearest brightness tile and compose it to the canvas
    for i in range(len(canvas.brightness)):
        
        # find the nearest brightness tile
        nearest_tile = FindNearestTiles(canvas.brightness[i], tiles)
        
        # compose the tile to the canvas
        for y in range(hight):
            for x in range(width):
                # map the tile index to the canvas
                iy = int(i / numberOfTileInCol) * hight + y
                ix = (i % numberOfTileInRow) * width + x
                
                # compose the tile to the canvas
                canvas.image[iy][ix] = nearest_tile[y][x]
   
    return canvas

# calculate the average brightness of the image
def average_brightness4image(image, width, hight):
    # get the size of the tile
    sizeOfTile = width * hight
    
    # total number of tiles
    totalNumberOfTile = (len(image) * len(image[0])) / sizeOfTile

    # create an array to store the brightness of each tile
    brightness = [0.0] * int(totalNumberOfTile)
    
    # number of tiles in a row
    numOfTileInRow = int(len(image[0]) / width)
    
    # get the color of the current image
    for y in range(len(image)):
        for x in range(len(image[y])):
            # calculate the tile number
            tileNumber = int(y / hight) * numOfTileInRow + int(x / width)
            
            # add the brightness to the tile
            brightness[tileNumber] += image[y][x]
            
    # calculate the average brightness
    for i in range(len(brightness)):
        brightness[i] = brightness[i] / sizeOfTile
    
    # return the average brightness
    return brightness

# enhancement function for photomosaic
def photomosaic_Cubic(canvas, tiles, W, H, w, h):
    # resize the canvas to the target width and height
    canvas = cubic_interpolation(canvas, W, H)
    
    # resize the tiles to the target width and height
    for i in range(len(tiles)):
        tiles[i] = cubic_interpolation(tiles[i], w, h)
    
    # convert the image to gray scale
    gray_canvas = image2brightness(canvas, w, h)

    # create a empty tile to store gray scale tiles
    tile_brightness = []
    
    # convert the tiles to gray scale
    for i in range(len(tiles)):
        tile_brightness.append(tile2brightness(tiles[i]))

    # Sort the tile_brightness array based on the brightness value
    tile_brightness.sort(key=lambda x: x.brightness)

    # compose the result image
    gray_canvas = ComposeTiles(gray_canvas, tile_brightness, w, h)
    return gray_canvas.image

def photomosaic_dithering_bilinear(canvas, tiles, W, H, w, h, size):

    # resize the canvas to the target width and height
    canvas = bilinear_interpolation(canvas, W, H)
    
    # resize the tiles to the target width and height
    for i in range(len(tiles)):
        tiles[i] = bilinear_interpolation(tiles[i], w, h)
    
    # convert the image to gray scale
    gray_canvas = image2brightness(canvas, w, h)

    # dithering process
    gray_canvas.image = Dithering(gray_canvas, size)
    
    # recaluclate the brightness of the dithering result
    gray_canvas.brightness = average_brightness4image(gray_canvas.image, w, h)
    
    # create a empty tile to store gray scale tiles
    tile_brightness = []
    
    # convert the tiles to gray scale
    for i in range(len(tiles)):
        tile_brightness.append(tile2brightness(tiles[i]))
    
    # Sort the tile_brightness array based on the brightness value
    tile_brightness.sort(key=lambda x: x.brightness)

    # compose the result image
    gray_canvas = ComposeTiles(gray_canvas, tile_brightness, w, h)

    return gray_canvas.image

def ditheringOnly(canvas, size):
    # convert the image to gray scale
    gray_canvas = image2brightness(canvas, 1, 1)
    # dithering process
    gray_canvas.image = Dithering(gray_canvas, size)
    return gray_canvas.image