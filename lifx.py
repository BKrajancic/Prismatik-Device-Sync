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

    last_set = 0, 0, 0
    while True:
        current_set = _get_average_hsv(connection)
        if any(map(0.05.__lt__, map(abs, map(operator.sub, last_set, current_set)))):
            last_set = current_set
            current_set = [round(val * max_val) for val in current_set]
            current_set.append(8000)
            bulb.set_color(current_set, rapid=True)

            time.sleep(0.05)
        else:
            time.sleep(0.01)


if __name__ == "__main__":
    _main()