
from HSVSource import HSVSource
from typing import Tuple
import socket
import itertools
import socket
import statistics
import colorsys
import os
import json
from operator import itemgetter


class PrismatikSource(HSVSource):
    def __init__(self, gamma_correction: float = 1.0):
        self._connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connection.connect(("127.0.0.1", 3636))
        self._connection.recv(8192)

        self._gamma_correction = gamma_correction

        configFilepath = "PrismatikConfig.json"
        if os.path.exists(configFilepath):
            with open(configFilepath, 'r') as f:
                config = json.load(f)
                self._led_start = config["LedStart"]
                self._led_end = config["LedEnd"]

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

        return zip(
            *(tuple(
                map(
                    str.split,
                    itertools.islice(entries, self._led_start, self._led_end),
                    itertools.repeat(","),
                )
            ))
        )


    def get_hsv(self) -> Tuple[float, float, float]:
        """
        Returns HSV. Get the average color of every led, by averaging the RGB values.

        Gamma_correction is what gamma correction to apply. "1.0" means none.
        """
        r, g, b = self._get_leds()

        r = map(int, r)
        g = map(int, g)
        b = map(int, b)

        r_mean = statistics.mean(r)
        g_mean = statistics.mean(g)
        b_mean = statistics.mean(b)

        h, s, v = colorsys.rgb_to_hsv(r_mean / 255, g_mean / 255, b_mean / 255)
        return h, s, v
