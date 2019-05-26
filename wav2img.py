import wave
from sys import argv
from PIL import Image, ImageDraw, ImageSequence
from itertools import zip_longest, chain
from math import sqrt

#https://audiocoding.ru/article/2008/05/22/wav-file-structure.html
def main():
    input_filename = argv[1]
    #input_filename = 'water_drops.wav'
    samples = get_samples(input_filename, 4096)
    colors = list([(i,i,i) for i in samples])
    image = make_square_image(int(sqrt(len(colors))), colors)
    #image = make_line_image(colors)
    image.save('test_cnock.png', 'PNG')
    

def get_samples(filename, n=None):
    f = open(filename,'rb')
    byte_per_sample = get_num_bit_per_sample(f) //8
    num_of_channels = get_num_of_channels(f)
    data = get_data(f)
    f.close()
    one_channel_samples = list(grouper(data, byte_per_sample))
    all_channel_samples = list(grouper(one_channel_samples, num_of_channels))
    list_of_list_of_sum = [ [sum(j) for j in i] for i in all_channel_samples ]
    merged_list = list(chain.from_iterable(list_of_list_of_sum))
    list_of_averages = list([i // (byte_per_sample*num_of_channels) for i in merged_list])
    return(list_of_averages)
    

#from doc
def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

def get_num_bit_per_sample(wav_file):
    wav_file.seek(34)
    return(int.from_bytes(wav_file.read(2), byteorder='little'))

def get_num_of_channels(wav_file):
    wav_file.seek(22)
    return(int.from_bytes(wav_file.read(2), byteorder='little'))

def get_data(wav_file):
    part_size = 1024
    file_size = wav_file.seek(0, 2)
    wav_file.seek(44)
    parts_of_file = []
    for i in range(0, file_size//part_size):
        info = wav_file.read(part_size)
        parts_of_file.append(info)
    return(list(chain.from_iterable(parts_of_file)))

def make_square_image(image_size, s_bytes_tuples):
    pic = Image.new('RGB', (image_size, image_size), (255, 255, 255))
    d = ImageDraw.ImageDraw(pic)
    for i in range(0, int(image_size)):
        for j in range(0, int(image_size)):   
            current_pic = i*image_size + j
            current_color = s_bytes_tuples[current_pic]
            d.point(xy=[(j, i)], fill=current_color)
    return pic

def make_line_image(s_bytes_tuples):
    image_size = len(s_bytes_tuples)
    pic = Image.new('RGB', (image_size,0), (255, 255, 255))
    d = ImageDraw.ImageDraw(pic)
    for i in range(0,image_size):
        current_color = s_bytes_tuples[i]
        d.point(xy=[(i, 0)], fill=current_color)
    return pic


if __name__ == "__main__":
    main()