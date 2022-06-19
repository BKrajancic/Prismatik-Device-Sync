from ctypes.wintypes import RGB
from tkinter import W
from pyrgbdev import Razer
from colorsys import hsv_to_rgb
from HSVSink import HSVSink
import itertools
import os
import time
import psutil
import json
from datetime import datetime
from operator import mul

from openrgb import OpenRGBClient
from openrgb.utils import RGBColor, DeviceType

def openRGB_running() -> bool:
    """Returns true if OpenRGB is running."""
    processes = list(map(lambda x: x.name(), psutil.process_iter()))
    return "OpenRGB.exe" in processes

def set_color_for(devices):
    def set_color(rgbColor: RGBColor):
        for device in devices:
            device.set_color(rgbColor)

    return set_color



class OpenRGBSink(HSVSink):
    def __init__(self) -> None:
        while not openRGB_running():
            time.sleep(10)

        self._client = OpenRGBClient()

        configFilepath = "OpenRGBConfig.json"
        self.set_color = lambda x: self._client.set_color(x, True)

        if os.path.exists(configFilepath):
            with open(configFilepath, 'r') as f:
                config = json.load(f)
                device_ids = set(config["device_id"])
                if len(device_ids) != len(self._client.devices):
                    devices = list(map(self._client.devices.__getitem__, device_ids))
                    self.set_color = set_color_for(devices)


    def send(self, hue: int, saturation: int, value: int) -> None:
        rgb = hsv_to_rgb(hue, saturation, value)
        rgb = map(mul, itertools.repeat(255), rgb)
        rgb = map(round, rgb)
        rgb = RGBColor(*tuple(rgb))
        self.set_color(rgb)

if __name__ == "__main__":
    openRGB_running()