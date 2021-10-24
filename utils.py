import itertools
from mss import mss
import socket
import statistics
import colorsys
import itertools
import time
from PIL import ImageGrab
from operator import itemgetter
from typing import Tuple
import socket
import numpy

from PIL.Image import Image

def get_connection():
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect(("127.0.0.1", 3636))
    connection.recv(8192)
    return connection

def get_leds(connection: socket.socket):
    connection.send(str.encode("getcolors\n"))
    data = connection.recv(8192)
    string = data.decode().split(":", 1)[1][:-3]
    entries = map(
        itemgetter(1), map(str.split, string.split(";"), itertools.repeat("-"))
    )

    entries = list(entries)
    divisor = 1
    r, g, b = zip(
        *tuple(
            map(
                str.split,
                list(entries)[: len(entries) // divisor],
                itertools.repeat(","),
            )
        )
    )
    return r, g, b


def _get_average_rgb(connection) -> Tuple[float, float, float]:
    r, g, b = get_leds(connection)
    geometric_mean = False
    if geometric_mean:
        r = [1 if value == "0" else int(value) for value in r]
        g = [1 if value == "0" else int(value) for value in g]
        b = [1 if value == "0" else int(value) for value in b]

        r_mean = statistics.geometric_mean(r)
        g_mean = statistics.geometric_mean(g)
        b_mean = statistics.geometric_mean(b)
    else:
        r_mean = statistics.mean(map(int, r))
        g_mean = statistics.mean(map(int, g))
        b_mean = statistics.mean(map(int, b))

    h, s, v = colorsys.rgb_to_hsv(r_mean / 255, g_mean / 255, b_mean / 255)
    return h, s, v


def _get_average_hsv(connection):
    r, g, b = get_leds(connection)
    r = [float(val) / 255 for val in r]
    g = [float(val) / 255 for val in g]
    b = [float(val) / 255 for val in b]
    h, s, v = zip(*list(map(colorsys.rgb_to_hsv, r, g, b)))
    # v = [0 if val < 20 else val for val in v]
    return (statistics.mean(h), statistics.mean(s), statistics.mean(v))

def capture_screenshot():
    # Capture entire screen
    with mss() as sct:
        img_t = numpy.array(sct.grab(sct.monitors[1])).T
        return numpy.mean(numpy.mean(img_t, axis=1), axis=1)


def _screengrab_average():
    t1 = time.time()
    img = capture_screenshot()
    t2 = time.time()
    print ("- Time %2.4f" % (t2-t1))
    b = img[0]
    g = img[1]
    r = img[2]
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    return h, s, v
