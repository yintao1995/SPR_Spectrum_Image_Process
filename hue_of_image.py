# _*_ coding:utf-8 _*_
"""
Calculate hue value/distribution of a given RGB image.
"""
from PIL import Image
import matplotlib.pyplot as plt


def rgb_to_hsv(r, g, b):
    """
    Calculate according to the formula equation.

    :param r:   red value
    :param g:  green value
    :param b:   blue value
    :return:    hue value
    """
    max_rgb = max(r, g, b)
    min_rgb = min(r, g, b)
    d = max_rgb - min_rgb
    v = max_rgb
    if d == 0:
        return 0.0, 0.0, v
    s = d / max_rgb
    if max_rgb == r:
        # pure red -> hue = 0
        h = (g - b)/d*60 + 0
    elif max_rgb == g:
        # pure green -> hue = 120
        h = (b - r)/d*60 + 120
    else:
        # pure blue -> hue = 240
        h = (r - g)/d*60 + 240
    if h < 0:
        h = h + 360
    return round(h, 2), s, v


def hue_of_image(path, *my_box):
    """
    Given a image file and selection parameters,
    Return it's hue value and hue distribution.
    About the para: my_box, it contains 4 numbers in format like below:
    (x of upper left corner, y of upper left corner, width , height ) in pixels.
    """
    filename = path
    im = Image.open(filename)
    if my_box and len(my_box) == 4:
        # print(my_box)
        box = (my_box[0], my_box[1], my_box[0] + my_box[2], my_box[1] + my_box[3])
        im = im.crop(box)
    pix = im.load()
    width = im.size[0]
    height = im.size[1]
    sum_hue = 0
    hue_matrix = [[0 for _ in range(width)] for _ in range(height)]
    for x in range(width):
        for y in range(height):
            r, g, b = pix[x, y][0:3]
            # sometimes it return 4 numbers, and the last is 255. why ?
            single_hue = rgb_to_hsv(r, g, b)[0]
            hue_matrix[y][x] = single_hue
            sum_hue += single_hue
    average_hue = round(sum_hue / (width * height), 2)
    # print(average_hue)
    return average_hue, hue_matrix


def draw_image(filename, average_hue, matrix):
    """
    Display 2-D image from hue matrix.
    """
    plt.figure(filename)
    plt.imshow(matrix, cmap=plt.get_cmap('rainbow'), vmin=0, vmax=360)
    plt.colorbar()
    plt.axis('off')
    plt.title("average_hue="+("%.2f" % average_hue))
    # plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    # plt.show()


if __name__ == '__main__':
    data = hue_of_image("C:\\Users\\yintao\\PycharmProjects\\SPR_System\\Test_Data\\1.png", 0, 0, 100, 100)
    draw_image("1.png", data[0], data[1])
    plt.show()
