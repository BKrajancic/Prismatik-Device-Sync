import time
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
        hue, saturation, value = _get_average_hsv(connection)

        hue *= max_val 
        hue = round(hue)

        saturation *= max_val 
        saturation = round(saturation)

        value *= max_val
        value = round(value)

        current_set = hue, saturation, value
        deltas = [
            abs(lhs - rhs) > max_val * 0.2
            for lhs, rhs in zip(last_set, current_set)
        ]
        if True in deltas:
            last_set = current_set
            bulb.set_color([hue, saturation, value, 8000], rapid=True)

        time.sleep(0.01)


if __name__ == "__main__":
    _main()