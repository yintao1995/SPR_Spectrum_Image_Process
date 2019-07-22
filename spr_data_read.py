# _*_ coding:utf-8 _*_
"""
Read SPR spectrum data and seek it's resonance wavelength.
"""
import matplotlib.pyplot as plt
import numpy as np


def read_data(file_path, sep, fn=''):
    """
    Read spectrum data from spectrum file(support .jdx or .txt ).

    :param file_path:    str, absolute or relative file path
    :param sep:     str, separator, ',' for .jdx file, and ' ' for .txt file.
    :param fn:
    :return:
    """
    if fn:
        filename = file_path + '/' + fn
    else:
        filename = file_path
    x_data = []
    y_data = []
    with open(filename, 'r', encoding='UTF-8') as file_obj:
        for line in file_obj.readlines():
            temp = line.strip().split(sep)
            try:
                x_data.append(float(temp[0].strip()))
                y_data.append(float(temp[1].strip()))
            except ValueError:
                pass
    return x_data, y_data


def visual_data(spectrum_data, section=None):
    """
    Calculate the resonance wavelength of given data (x[], y[]),
    Accept 'section' parameter to manually correct errors.

    :param spectrum_data:  Tuple -- (x[], y[])
    :param section:  Tuple -- (r1, r2)
    :return:
    """
    # sampling
    sampling_rate = 5
    x_data = spectrum_data[0]
    x1 = [x_data[i] for i in range(0, len(x_data), sampling_rate)]
    y_data = spectrum_data[1]
    y1 = [y_data[i] for i in range(0, len(y_data), sampling_rate)]

    # normalize
    y_max = max(y1)
    n_y1 = [ai/y_max for ai in y1]
    ymax = max(y_data)
    n_y = [ai/ymax for ai in y_data]

    # smooth
    smooth_order = 6
    for i in range(smooth_order):
        n_y1 = mean_smooth(n_y1)

    # Firstly, find a rough estimate of resonance wavelength(relative minimum value).
    # Secondly, if a rough estimate is found, take a section around it out for fitting.
    if not section:
        temp = find_min(n_y1, sampling_rate)
        # print('temp:',temp)
        if not temp:
            return x_data, n_y, 0

        length = 20
        index = cut_list(x1, x1[temp[0]]-length, x1[temp[0]]+length)
        cut_x = x_data[sampling_rate*index[0]: sampling_rate*index[1]]
        cut_y = n_y[sampling_rate*index[0]: sampling_rate*index[1]]
    else:
        index = cut_list(x_data, section[0], section[1])
        cut_x = x_data[index[0]:index[1]]
        cut_y = n_y[index[0]:index[1]]

    # fitting
    cut_x = np.array(cut_x)
    cut_y = np.array(cut_y)
    z1 = np.polyfit(cut_x, cut_y, 4)
    p1 = np.poly1d(z1)
    # print(p1)
    fitted_y = p1(cut_x)

    # find minimum
    min_y = min(fitted_y)
    resonance_wavelength = 0
    resonance_amplitude = 0
    for i in range(0, len(cut_x)):
        if fitted_y[i] == min_y:
            resonance_wavelength = cut_x[i]
            resonance_amplitude = cut_y[i]
            break
    return x_data, n_y, resonance_wavelength, resonance_amplitude


def cut_list(list_a, x1, x2):
    """
    Give an increasing sequence, find the chosen section which satisfy: x1<x<x2.

    :param list_a:   List[num]
    :param x1:       num
    :param x2:       num
    :return:    Tuple, index at start and end
    """
    index1 = index2 = 0
    for i in range(len(list_a)):
        if list_a[i] < x1:
            pass
        else:
            index1 = i
            break
    if list_a[-1] < x2:
        return index1, -1
    for i in range(index1, len(list_a)):
        if list_a[i] < x2:
            pass
        else:
            index2 = i
            break
    return index1, index2


def mean_smooth(data_y):
    """Median Filter
    Smooth the data before next step of processing to reduce errors
    :param data_y:  List[num]
    :return:               List[num]
    """
    temp = data_y
    for i in range(1, len(data_y) - 1):
        temp[i] = (data_y[i - 1] + data_y[i + 1]) / 2
    return temp


def find_min(list_a, sampling):
    """
    rough estimate of relative minimum value
    """
    for i in range(round(500 / sampling), len(list_a) - round(250 / sampling)):
        if list_a[i - 1] < list_a[i] or list_a[i + 1] < list_a[i]:
            pass
        else:
            if list_a[i - round(50 / sampling)] > list_a[i] and list_a[i + round(50 / sampling)] > list_a[i]:
                return i, list_a[i]


if __name__ == "__main__":
    path = "D:\\学习！学习！学习！学习！\\电子所里的研二\\实验数据\\20181116_LX_TiO2\\data\\10_00.txt"
    data = visual_data(read_data(path, '\t'))
    fig = plt.figure(figsize=(10, 5), dpi=100)
    plt.plot(data[0], data[1])
    plt.axvline(data[2], c='red', alpha=0.5)
    # plt.text(500 , 0.2, "resonance wavelength="+str(data[2])+"nm")
    plt.text(500, 0.2, "resonance wavelength="+str(data[2])+"nm")
    # label = ['-12°']
    # plt.legend(label)
    plt.show()
