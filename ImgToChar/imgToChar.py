#!/usr/bin/env python
# -*-coding:utf-8 -*-

# loading package
import argparse
from PIL import Image
import string
import os
import re

# TODO: Get the argument with user interactive

## define the argument parser
parser = argparse.ArgumentParser(
    usage="Convert Img to char", description="Get the img file and output file"
)
## ⏰append action builds file list
parser.add_argument(
    "-f", "--file", action="append", 
    help="img file or list of img files. eg:-f file1 -f file2"
)
parser.add_argument("--width", type=int, default=100)
parser.add_argument("--height", type=int, default=100)

## ⏰if required True, must specify the argument
parser.add_argument("-o", "--output", required=False)


# TODO: Store the argument
args = parser.parse_args()
CHAR = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
IMAGE = args.file
OUTPUT = args.output
WIDTH = args.width
HEIGHT = args.height

# TODO: Transform RGB as grey
def __scale_pixel(file, width=WIDTH, height=HEIGHT, resize=False, crop=False):
    # TODO: open image
    img = Image.open(file)

    # TODO: check whether the arguments width and height are right
    # Cutting or resizing image
    # rescale the image
    if True in [resize, crop]:
        width = min([width, img.size[0]])
        height = min([height, img.size[1]])
    else:
        width, height = img.size

    if resize and crop:
        raise ValueError("Arguments resize and crop are True. Choose one method!")

    # crop image
    if crop:
        img = img.crop((width, height))
    if resize:
        img = img.resize((width, height), Image.NEAREST)

    # get the grey image
    img = img.convert("L")

    return (width, height), img

# TODO: Transform the img to text
def __transform(file, verbose=True, output=None, save=False, report=False, **argv):
    _, img = __scale_pixel(file, **argv)
    # img.show()
    result = ""
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            index = int(img.getpixel((x,y)) / 257.0 * len(CHAR))
            result += CHAR[index]
        result += "\n"
    
    if verbose:
        print(result)
    
    if report:
        img.show()
    
    if save:
        try:
            if output is None:
                output = re.sub(r"\.[a-z]+", ".txt", file)
            elif not output.endswith(".txt"):
                output = os.path.join(output, re.sub(r"\.[a-z]+", ".txt", file))
        except AttributeError as err:
            print(err + "Need store filename")
            output = input("Plz enter text file name: ")
            while not output.endswith(".txt"):
                print("Enter a file tail name is .txt!")
                output = input("Plz enter text file name: ")
        
        with open(output, "w") as file:
            file.write(result)

if __name__ == "__main__":
    __transform(IMAGE[0], resize=True)