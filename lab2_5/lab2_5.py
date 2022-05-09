import matplotlib.pyplot as plt
import pandas as pd
import math
import random
import numpy as np

#метод наименьших квадратов
def mnk(x, y):
    x_square = 0
    xy_average = 0
    count = len(x)
    for i in range(count):
        xy_average += x[i] * y[i]
        x_square += x[i]**2

    a = (sum(x) * sum(y) - count * xy_average) / (sum(x)**2 - count * x_square)
    b = (sum(x) * xy_average - x_square * sum(y)) / (sum(x)**2 - count * x_square)
    return (a, b)

#main
def fill_file():
    print("Введите шаг начало и конец")
    step, start, finish =  map(float, input().split())
    x = []
    y1 = []
    y2 = []
    y3 = []
    i = start
    while i < finish:
        i += step
        x.append(i)
        y1.append(math.sin(i) + 0.1 * math.sin(i**5))
        y2.append(math.cos(i))
        y3.append(math.tan(i) * 0.5)

    fig, ax = plt.subplots(3, 1)
    df = pd.DataFrame({"x1": x, "y1": y1, "y2": y2, "y3": y3})
    df.to_excel('./list.xlsx')
    read_file(2, ax[0])
    read_file(3, ax[1])
    read_file(4, ax[2])
    plt.show()

#чтение файла
def read_file(column_y, ax):
    x = []
    y = []
    res = pd.read_excel("./list.xlsx", usecols = [1, column_y])
    for i in res[res.keys()[1]]: y.append(i)
    for i in res[res.keys()[0]]: x.append(i)

    a, b = mnk(x, y)
    sm_y = smoothing(y, 0.12)
    bet_y = bet(y, x)

    ax.plot([x[0], x[-1]], [x[0] * a + b, x[-1] * a + b], color = "grey", label = "MNK")
    ax.plot(x, y, color = "green", label = "Normal")
    ax.plot(x, sm_y, color = "blue", label = "Smoothing")
    ax.plot(x, bet_y, color = "black", label = "Forecast")
    ax.legend()

#сглаживание динамическим окном
def smoothing(array, k):
    res = []
    for i in range(len(array)): res.append(smoothing_for_element(array[:i + 1], k))
    return res

#сглаживание для 1 элемента
def smoothing_for_element(window, k):
    while math.fabs((window[-1] - (sum(window) / len(window))) / window[-1]) > k: window.pop(0)
    return sum(window) / len(window)

#предсказания
def bet(y, x):
    res = y[0:2]
    for i in range(2, len(y)):
        k = (y[i - 1] - y[i - 2]) / (x[i - 1] - x[i - 2])
        b = y[i - 1] - k * x[i - 1]
        res.append(x[i] * k + b)
    return res

fill_file()
