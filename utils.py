import itertools
import operator
import socket
import statistics
import colorsys
import time
import json
from operator import itemgetter, truediv
from typing import Tuple
import socket

def get_connection():
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect(("127.0.0.1", 3636))
    connection.recv(8192)
    return connection

def is_on(connection: socket.socket) -> bool:
    connection.send(str.encode("getstatus\n"))
    data: str = connection.recv(8192).decode().strip()
    return data == "status:on"

def get_leds(connection: socket.socket):
    """Get leds from prismatik."""
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


def _get_average_rgb(connection, gamma_correction: float, nth: int) -> Tuple[float, float, float]:
    """
    Returns HSV. Get the average color of every led, by averaging the RGB values.

    Gamma_correction is what gamma correction to apply. "1.0" means none.
    """
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
        r = map(int, r)
        g = map(int, g)
        b = map(int, b)
        if gamma_correction != 1.0:
            max_val = 255
            r = [max_val * pow(val / max_val, gamma_correction) for val in r]
            g = [max_val * pow(val / max_val, gamma_correction) for val in g]
            b = [max_val * pow(val / max_val, gamma_correction) for val in b]

        r_mean = statistics.mean(r)
        g_mean = statistics.mean(g)
        b_mean = statistics.mean(b)

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

def _get_median_hsv(connection):
    r, g, b = get_leds(connection)
    r = [int(val) / 255 for val in r]
    g = [int(val) / 255 for val in g]
    b = [int(val) / 255 for val in b]

    h, s, v = zip(*list(map(colorsys.rgb_to_hsv, r, g, b)))
    # v = [0 if val < 20 else val for val in v]
    return (statistics.median(h), statistics.median(s), statistics.median(v))

def _get_median_rgb(connection) -> Tuple[float, float, float]:
    r, g, b = get_leds(connection)
    r_median = statistics.median(map(int, r))
    g_median = statistics.median(map(int, g))
    b_median = statistics.median(map(int, b))

    h, s, v = colorsys.rgb_to_hsv(r_median / 255, g_median / 255, b_median / 255)
    return h, s, v

