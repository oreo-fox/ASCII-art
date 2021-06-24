import os
import sys
import math
import PIL
from PIL import Image
import numpy as np

# open the image
def load_image(img_path, max_width):

    try:
        image = Image.open(img_path)
        image = resize(image, max_width)
        width, height = image.size
        print("Opened Image: " + img_path + " with size(w x h): " + str(width) + " " + str(height) )
        return image, width, height

    except IOError:
        print("Could not open image!")
        return None

#convert the image to am array
def convert_image(image, width, height):

    #get the rgb values
    data = image.getdata()
    pixel_array = np.array(data)

    #covert to luminance as seen on https://en.wikipedia.org/wiki/Relative_luminance
    lum_array = np.zeros(width*height)
    i = 0
    for pixel in pixel_array:
        lum = 0.2126 * pixel[0] + 0.7152 * pixel[1] + 0.0722 * pixel[2]
        lum_array[i] = math.ceil(lum)
        i += 1

    lum_array = np.reshape(lum_array, (height, width))

    return lum_array

#map the luminance values to ASCII chars
def map_ascii(lum_matrix):

    ascii = '`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'
    ascii_size = len(ascii) - 1
    row, col = lum_matrix.shape

    # dtype U1 for one char (unicode points because python3)
    ascii_matrix = np.zeros(row * col, 'U1')

    lum_matrix = lum_matrix.flatten()
    i = 0
    for lum in lum_matrix:
        char_num = int((ascii_size / 255) * lum)
        char = ascii[char_num]
        ascii_matrix[i] = char
        i += 1
    
    ascii_matrix = np.reshape(ascii_matrix,(row, col))

    return ascii_matrix

def print_ascii(ascii_matrix):

    for line in ascii_matrix:
        str_line = ""
        for c in line:
            str_line = str_line + c*2
        
        print(str_line)


def resize(image, max_width):
   
    wpercent = (max_width/float(image.size[0]))
    hsize = int((float(image.size[1])*float(wpercent)))
    image = image.resize((max_width,hsize), PIL.Image.ANTIALIAS)

    return image
        
        
if __name__ == "__main__":

    
    if len(sys.argv) == 2:
        img_path = sys.argv[1]

        img = load_image(img_path, 50)
    
        if img is not None:
            array = convert_image(img[0], img[1], img[2])
            ascii_matrix = map_ascii(array)
            print_ascii(ascii_matrix)
    
    elif len(sys.argv) == 3:
        img_path = sys.argv[1]
        max_width = sys.argv[2]

        img = load_image(img_path, max_width)
    
        if img is not None:
            array = convert_image(img[0], img[1], img[2])
            ascii_matrix = map_ascii(array)
            print_ascii(ascii_matrix)
    
    else:
        print("Ooops! something went wrong!")
        print("Please use the following commands: ascii.py path_to_image or ascii.py path_to_image max_width")


    
    

    
    
    


