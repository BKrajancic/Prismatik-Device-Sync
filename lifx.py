import time
import operator
from utils import get_connection, _get_average_hsv, _get_average_rgb, _get_median_hsv
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
    kelvin_range = [bulb.get_min_kelvin(), bulb.get_max_kelvin()]
    while True:
        # current_set = _get_average_hsv(connection)
        current_set = _get_median_hsv(connection)
        potential_set = _get_average_rgb(connection)
        current_set = list(potential_set)
        if current_set[1] < 0.05:
            current_set[1] = 0
        # if current_set[2] < 0.1:
        #     current_set[2] = 0
        current_set = list(current_set)
        thresholds = 0.05, 0.25, 0.25
        deltas = map(abs, map(operator.sub, last_set, current_set))

        if True or any(map(operator.gt, deltas, thresholds)):
            kelvin_val = kelvin_range[1]
            pure_white = current_set[1] < 0.01
            if current_set[0] not in [0.0, 0] and not pure_white:
                kelvin_val = (
                    0.5 - (current_set[0] - 0.5)
                    if current_set[0] > 0.5
                    else current_set[0]
                )

                kelvin_val *= kelvin_range[1] - kelvin_range[0]
                kelvin_val += kelvin_range[0]
                kelvin_val += 1500  # Leads to better browns imo.

            last_set = current_set
            current_set = [round(val * max_val) for val in current_set]
            current_set.append(kelvin_val)

            bulb.set_color(current_set, rapid=True)

            time.sleep(0.01)
        else:
            time.sleep(0.01)


if __name__ == "__main__":
    _main()
