
from HSVSource import HSVSource
from typing import Tuple
import socket
import itertools
import socket
import statistics
import colorsys
from operator import itemgetter, truediv


class PrismatikSource(HSVSource):
    def __init__(self, gamma_correction: float = 1.0):
        self._connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connection.connect(("127.0.0.1", 3636))
        self._connection.recv(8192)

        self._gamma_correction = gamma_correction

    def is_running(self) -> bool:
        self._connection.send(str.encode("getstatus\n"))
        data: str = self._connection.recv(8192).decode().strip()
        return data == "status:on"

    def _get_leds(self):
        """Get leds from prismatik."""
        self._connection.send(str.encode("getcolors\n"))
        data = self._connection.recv(8192)
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


    def get_hsv(self) -> Tuple[float, float, float]:
        """
        Returns HSV. Get the average color of every led, by averaging the RGB values.

        Gamma_correction is what gamma correction to apply. "1.0" means none.
        """
        r, g, b = self._get_leds()

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
            if self._gamma_correction != 1.0:
                max_val = 255
                r = [max_val * pow(val / max_val, self.gamma_correction) for val in r]
                g = [max_val * pow(val / max_val, self.gamma_correction) for val in g]
                b = [max_val * pow(val / max_val, self.gamma_correction) for val in b]

            r_mean = statistics.mean(r)
            g_mean = statistics.mean(g)
            b_mean = statistics.mean(b)

        h, s, v = colorsys.rgb_to_hsv(r_mean / 255, g_mean / 255, b_mean / 255)
        return h, s, v
