from tkinter import W
from pyrgbdev import Razer
from colorsys import hsv_to_rgb
from HSVSink import HSVSink
import itertools
import time
import psutil
from datetime import datetime
from operator import mul

from openrgb import OpenRGBClient
from openrgb.utils import RGBColor, DeviceType

def openRGB_running() -> bool:
    """Returns true if OpenRGB is running."""
    processes = list(map(lambda x: x.name(), psutil.process_iter()))
    return "OpenRGB.exe" in processes

class OpenRGBSink(HSVSink):
    def __init__(self) -> None:
        while not openRGB_running:
            time.sleep(10)

        self._client = OpenRGBClient()

    def send(self, hue: int, saturation: int, value: int) -> None:
        rgb = hsv_to_rgb(hue, saturation, value)
        rgb = map(mul, itertools.repeat(255), rgb)
        rgb = map(round, rgb)
        rgb = tuple(rgb)
        for device in self._client.devices:
            device.set_color(RGBColor(*rgb))

if __name__ == "__main__":
    openRGB_running()