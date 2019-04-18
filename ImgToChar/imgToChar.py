#!/usr/bin/env python
# -*-coding:utf-8 -*-

# loading package
import argparse
from PIL import Image
import string

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
CHAR = string.printable.replace(" ", "")
IMAGE = args.file
OUTPUT = args.output
WIDTH = args.width
HEIGHT = args.height

print(args)
# TODO: Transform RGB as grey
def __scale_pixel(image, width=WIDTH, height=HEIGHT, resize=False, crop=False):
    # TODO: open image
    img = Image.open(image)

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
        img = img.resize((width, height))

    # get the grey image
    img = img.convert("L")

    return (width, height), img
