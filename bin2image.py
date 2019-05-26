from sys import argv
from PIL import Image, ImageDraw, ImageSequence
from math import sqrt
from itertools import zip_longest, repeat
import imageio

def main():
    input_filename = argv[1]
    file_bytes = get_bytes(input_filename)
    file_bytes_tuples = list(grouper(file_bytes, 3, bytes(0)))
    image_size = get_image_size(file_bytes_tuples)

    if argv[2]=='--png':
        if len(argv) < 4:
            out_filename = input_filename + '_.png'
        else:
            out_filename = argv[3]
        pic = make_image(image_size, file_bytes_tuples)
        pic.save(out_filename, 'PNG')
    elif argv[2]=='--gif':
        if len(argv) > 4:
            if argv[3] == '-c':
                shots_count = int(argv[4])
                shot_size = int(image_size / shots_count)
                if len(argv) == 6:
                    out_filename = argv[5]
                elif len(argv) == 5:
                    out_filename = input_filename+'.gif'
        else:
            if len(argv) == 4:
                out_filename = argv[3]
            elif len(argv) == 3:
                out_filename = input_filename+'.gif'
            shots_count = int(image_size/100)
            shot_size = 100
        images = get_image_list(file_bytes_tuples, shot_size)
        imageio.mimsave(out_filename, images, duration = 0.04)


def get_bytes(filename):
    s = open(filename, 'rb')
    return s.read()


def get_image_size(bytes_list):
    return int(sqrt(len(bytes_list)))


def get_image_list(s_bytes_tuples, shot_size):
    images_bytes_list = list(grouper(s_bytes_tuples, shot_size**2, (0,0,0)))
    
    return [make_image(int(shot_size), list(image_bytes)) for image_bytes in images_bytes_list]


#from doc
def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def make_image(image_size, s_bytes_tuples):
    pic = Image.new('RGB', (image_size, image_size), (255, 255, 255))
    d = ImageDraw.ImageDraw(pic)
    for i in range(0, int(image_size)):
        for j in range(0, int(image_size)):   
            current_pic = i*image_size + j
            current_color = s_bytes_tuples[current_pic]
            d.point(xy=[(i, j)], fill=current_color)
    return pic


if __name__ == "__main__":
    main()
