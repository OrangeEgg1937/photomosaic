# implementation of the function `photomosaic`
# you are not allowed to use any third-party libraries

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

# bilinear interpolation for resizing the image for giving width and height

def bilinear_interpolation(image, width, hight):
    # get the original width and height
    H = len(image)
    W = len(image[0])
    
    # print the original width and height
    print(f"Width:{W}, Height:{H}")

    # get the ratio of the original image and the target image
    w_ratio = W / width
    h_ratio = H / hight
    
    # create a new image with the target width and height
    result = []
    
    for i in range(width):
        temp = []
        for j in range(hight):
            # get the original position of the target pixel
            x = int(i * w_ratio)
            y = int(j * h_ratio)
            # get the distance between the target pixel and the original pixel
            dx = i * w_ratio - x
            dy = j * h_ratio - y
            # get the value of the target pixel by bilinear interpolation
            temp.append((1 - dx) * (1 - dy) * image[x][y] + dx * (1 - dy) * image[x + 1][y] + (1 - dx) * dy * image[x][y + 1] + dx * dy * image[x + 1][y + 1])
        result.append(temp)
        
    return result


def photomosaic(canvas, tiles, W, H, w, h):
    
    # resize the canvas to the target width and height
    new_canvas = bilinear_interpolation(canvas, W, H)

    return RGB2Gray(canvas)