import time
import operator
from utils import get_connection, _get_average_hsv
from lifxlan import LifxLAN, Light

def _get_bulb() -> Light:
    lifxlan = LifxLAN()
    bulb: Light = lifxlan.get_color_lights()[0]
    return bulb

def _main():
    connection = get_connection()
    bulb = _get_bulb()

    max_val = 65535

    last_set = [0, 0, 0]
    while True:
        current_set = _get_average_hsv(connection)
        changes = list(map(0.05.__lt__, map(abs, map(operator.sub, last_set, current_set))))
        if False not in changes:
            current_set = [round(val * max_val) for val in current_set]
            last_set = current_set
            current_set.append(8000)
            bulb.set_color(current_set, rapid=True)
        else:
            if changes[0]:
                hue = round(current_set[0] * max_val)
                bulb.set_hue(hue, rapid=True)
                last_set[0] = hue
            if changes[1]:
                saturation = round(current_set[1] * max_val)
                bulb.set_saturation(saturation, rapid=True)
                last_set[1] = saturation
            if changes[2]:
                brightness = round(current_set[2] * max_val)
                bulb.set_brightness(brightness, rapid=True)
                last_set[2] = brightness


if __name__ == "__main__":
    _main()