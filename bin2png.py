from sys import argv
from PIL import Image, ImageDraw
from math import sqrt
from itertools import zip_longest


def main():
    input_filename = argv[1]
    if len(argv) < 3:
        image_filename = input_filename + '_.png'
    else:
        image_filename = argv[2]
    file_bytes = get_bytes(input_filename)
    file_bytes_tuples = list(grouper(file_bytes, 3, bytes(0)))
    image_size = get_image_size(file_bytes_tuples)
    make_image(image_filename, image_size, file_bytes_tuples)


def get_bytes(filename):
    s = open(filename, 'rb')
    return s.read()


def get_image_size(bytes_list):
    return int(sqrt(len(bytes_list)))

#from doc
def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def make_image(filename, image_size, s_bytes_tuples):
    pic = Image.new('RGB', (image_size, image_size), (255, 255, 255))
    d = ImageDraw.ImageDraw(pic)
    for i in range(0, image_size):
        for j in range(0, image_size):
            current_pic = i*image_size + j
            current_color = s_bytes_tuples[current_pic]
            d.point(xy=[(i, j)], fill=current_color)
    pic.save(filename, "PNG")


if __name__ == "__main__":
    main()
