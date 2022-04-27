from PyPeripheral import Razer
from colorsys import hsv_to_rgb
from HSVSink import HSVSink
import itertools
from operator import mul

class RazerSink(HSVSink):
    def __init__(self) -> None:
        self._sdk = Razer.SDK()
        self._sdk.connect()

    def send(self, hue: int, saturation: int, value: int) -> None:
        rgb = hsv_to_rgb(hue, saturation, value)
        rgb = map(mul, itertools.repeat(255), rgb)
        rgb = map(round, rgb)
        rgb = tuple(rgb)
        self._sdk.set_rgb({"ETC": rgb})

if __name__ == "__main__":
    # Quick demo
    r = Razer.SDK()
    r.connect()
    for i in range(10):
        _id = "ETC"
        r.set_rgb({_id: (255, 0, 0)})
        r.set_rgb({_id: (0, 255, 0)})
        r.set_rgb({_id: (0, 0, 255)})

