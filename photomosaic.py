# implementation of the function `photomosaic`
# you are not allowed to use any third-party libraries

import timeit

# create a empty dictionary to store the average color of each tile
tile_dictionary = {}

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

# self-define function to convert RGB to Gray
def RGB2Gray(canvas):
    # convert the canvas color to gary
    result = []
    for pixel in canvas:
        temp = []
        for i in range(len(pixel)):
            temp.append(0.299 * pixel[i][0] + 0.587 * pixel[i][1] + 0.114 * pixel[i][2])
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

    # create a new image with the target width and height
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

def photomosaic(canvas, tiles, W, H, w, h):
    
    start = timeit.default_timer()
    # resize the canvas to the target width and height
    new_canvas = bilinear_interpolation(canvas, W, H)
    stop = timeit.default_timer()
    print('Time: ', stop - start)  
    
    # resize the tiles to the target width and height
    tiles[1] = bilinear_interpolation(tiles[1], w, h)

    return new_canvas