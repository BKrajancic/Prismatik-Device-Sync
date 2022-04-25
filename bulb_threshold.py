"""wrap a bulb around this to prevent it always sending"""
from ctypes.wintypes import RGB
from rgb_device import RGBDevice
import operator


class BulbThreshold(RGBDevice):
    def __init__(self, rgbDevice: RGBDevice):
        self._send_only_on_change = False
        self._thresholds = 0.02, 0.02, 0.02

        self._gamma = 1.0
        self._min_brightness = 0.05

        # Bring this out perhaps.
        self._min_brightness_if_off = self._min_brightness * 3
        self._rgbDevice = rgbDevice
        self.max_val = 65535
        # max_val = 65535
        # is_off = True
        self._prev_hue = 0
        self._prev_sat = 0
        self._prev_val = 0
        self._is_off = False
        self._last_set = 0, 0, 0


    def send(self, hue: int, saturation: int, value: int) -> None:
        send_only_on_change = False
        current_set = [hue, saturation, value]

        if current_set[1] < 0.05:
            current_set[1] = 0

        if current_set[2] < self._min_brightness:
            current_set[2] = 0

        if self._is_off and current_set[2] < self._min_brightness_if_off:
            current_set[2] = 0

        deltas = map(abs, map(operator.sub, self._last_set, current_set))
        if not (send_only_on_change) or any(map(operator.gt, deltas, self.thresholds)):
            self._last_set = current_set

            if current_set[2] == 0:
                self._is_off = True
            elif self._is_off:
                self._is_off = False

            self._rgbDevice.send(*current_set)
