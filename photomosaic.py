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

def photomosaic(canvas, tiles, W, H, w, h):
    
    # process bilinear interpolation
    w_ratio = 

    return RGB2Gray(canvas)