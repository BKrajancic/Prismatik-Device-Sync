import itertools
import socket
import statistics
import colorsys
import time
import json
from operator import itemgetter
from typing import Tuple

from MilightWifiBridge import MilightWifiBridge


def get_leds(connection: socket.socket):
    connection.send(str.encode("getcolors\n"))
    data = connection.recv(8192)
    string = data.decode().split(":", 1)[1][:-3]
    entries = map(
        itemgetter(1), map(str.split, string.split(";"), itertools.repeat("-"))
    )

    entries = list(entries)
    divisor = 1
    r, g, b = zip(
        *tuple(
            map(
                str.split,
                list(entries)[: len(entries) // divisor],
                itertools.repeat(","),
            )
        )
    )
    return r, g, b


def _get_average_rgb(connection) -> Tuple[float, float, float]:
    r, g, b = get_leds(connection)
    geometric_mean = False
    if geometric_mean:
        r = [1 if value == "0" else int(value) for value in r]
        g = [1 if value == "0" else int(value) for value in g]
        b = [1 if value == "0" else int(value) for value in b]

        r_mean = statistics.geometric_mean(r)
        g_mean = statistics.geometric_mean(g)
        b_mean = statistics.geometric_mean(b)
    else:
        r_mean = statistics.mean(map(int, r))
        g_mean = statistics.mean(map(int, g))
        b_mean = statistics.mean(map(int, b))

    h, s, v = colorsys.rgb_to_hsv(r_mean / 255, g_mean / 255, b_mean / 255)
    return h, s, v


def _get_average_hsv(connection):
    r, g, b = get_leds(connection)
    r = [float(val) / 255 for val in r]
    g = [float(val) / 255 for val in g]
    b = [float(val) / 255 for val in b]
    h, s, v = zip(*list(map(colorsys.rgb_to_hsv, r, g, b)))
    # v = [0 if val < 20 else val for val in v]
    return (statistics.mean(h), statistics.mean(s), statistics.mean(v))


def _send_udp():
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect(("127.0.0.1", 3636))
    connection.recv(8192)

    with open("config.json", "r") as f:
        config = json.load(f)
    zoneId = config["zoneId"]
    milight = load_milight(config["ip"], config["port"], zoneId)
    delay = 0.1
    val_threshold = 0.05
    is_off = False
    last_hue = 0
    last_sat = 0
    last_val = 0
    while True:
        # triple = _get_average_rgb(connection)
        hue, saturation, val = _get_average_rgb(connection)
        # hue, saturation, val = _get_average_hsv(connection)
        triple = _get_average_hsv(connection)
        # print(triple)
        # hue, val, saturation = colorsys.rgb_to_hls(*_get_average())
        if (
            abs(hue - last_hue) > 0.05
            or abs(val - last_val) > 0.25
            or abs(saturation - last_sat) > 0.25
            or (is_off and val > val_threshold)
            or (not is_off and val < val_threshold)
        ):
            last_hue = hue
            last_sat = saturation
            last_val = val
            # val *= 3
            if is_off:
                if val > val_threshold:
                    milight.turnOn(zoneId=zoneId)
                    is_off = False
            elif val < val_threshold:
                milight.turnOff(zoneId=zoneId)
                is_off = True

            if not is_off:
                transmit_color(milight, zoneId, hue, saturation, val)

            time.sleep(delay)
        time.sleep(delay)


def load_milight(ip: str, port: int, zoneId: int):
    milight = MilightWifiBridge.MilightWifiBridge()
    milight.setup(ip=ip, port=port, timeout_sec=0.50)
    delay = 0.5
    milight.turnOn(zoneId=zoneId)
    time.sleep(delay)
    milight.setWhiteMode(zoneId)
    time.sleep(delay)
    milight.setTemperature(100, zoneId)
    time.sleep(delay)
    milight.setBrightness(brightness=100, zoneId=zoneId)
    time.sleep(delay)
    milight.setColor(0, zoneId)
    time.sleep(delay)
    milight.setSaturation(saturation=0, zoneId=zoneId)
    time.sleep(delay)
    milight.setBrightness(brightness=100, zoneId=zoneId)
    return milight


def transmit_color(
    milight: MilightWifiBridge.MilightWifiBridge,
    zoneId,
    hue: float,
    saturation: float,
    val: float,
):
    saturation_max = 100
    saturation_threshold = 15
    saturation_scaled = saturation * saturation_max
    if saturation_scaled < saturation_threshold:
        milight.setWhiteMode(zoneId)
    else:
        scaled_hue = hue * 255
        if scaled_hue > 250:
            milight.setColor(color=16, zoneId=zoneId)  # Probs needs more work.
            milight.setSaturation(saturation=100 - saturation_scaled, zoneId=zoneId)
        else:
            if scaled_hue < 68:
                scaled_hue += 0x0F
                scaled_hue %= 0xFF

            milight.setColor(color=scaled_hue, zoneId=zoneId)  # Probs needs more work.
            milight.setSaturation(saturation=100 - saturation_scaled, zoneId=zoneId)

    milight.setBrightness(brightness=val * 100, zoneId=4)  # Probs needs more work.

    # max_sat = 20
    # milight.setSaturation(saturation=100, zoneId=4)
    # milight.setSaturation(saturation=max_sat - (saturation * max_sat), zoneId=zoneId)


if __name__ == "__main__":
    _send_udp()
