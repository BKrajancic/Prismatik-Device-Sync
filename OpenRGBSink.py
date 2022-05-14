from pyrgbdev import Razer
from colorsys import hsv_to_rgb
from HSVSink import HSVSink
import itertools
from operator import mul

from openrgb import OpenRGBClient
from openrgb.utils import RGBColor, DeviceType

class OpenRGBSink(HSVSink):
    def __init__(self) -> None:
        self._client = OpenRGBClient()

    def send(self, hue: int, saturation: int, value: int) -> None:
        rgb = hsv_to_rgb(hue, saturation, value)
        rgb = map(mul, itertools.repeat(255), rgb)
        rgb = map(round, rgb)
        rgb = tuple(rgb)
        for device in self._client.devices:
            device.set_color(RGBColor(*rgb))
