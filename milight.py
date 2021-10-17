import itertools
import socket
import statistics
import colorsys
import time
import json
from operator import itemgetter

import lightpack
from MilightWifiBridge import MilightWifiBridge

def _get_average(connection):
    connection.send(str.encode('getcolors\n'))
    data = connection.recv(8192)
    string = data.decode().split(":", 1)[1][:-3]
    entries = map(itemgetter(1), map(str.split, string.split(";"), itertools.repeat('-')))
    # First 24 entries for just left side.
    entries = list(entries)

    r, g, b = zip(*tuple(map(str.split, list(entries)[:len(entries) // 2], itertools.repeat(','))))
    geometric_mean = False
    if geometric_mean:
        r = [1 if value == '0' else int(value) for value in r]
        g = [1 if value == '0' else int(value) for value in g]
        b = [1 if value == '0' else int(value) for value in b]
        return (
            statistics.geometric_mean(r) / 255,
            statistics.geometric_mean(g) / 255,
            statistics.geometric_mean(b) / 255
        )
    else:
        return (
            statistics.mean(map(int, r)) / 255,
            statistics.mean(map(int, g)) / 255,
            statistics.mean(map(int, b)) / 255
        )
def _send_udp():
    with open("config.json", 'r') as f:
        config = json.load(f)
    ip = config["ip"]
    port = config["port"]
    zoneId = config["zoneId"]

    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect(("127.0.0.1", 3636))
    connection.recv(8192)

    milight = MilightWifiBridge.MilightWifiBridge()
    milight.setup(ip=ip, port=port, timeout_sec=0.50)
    delay = 0.1
    milight.turnOn(zoneId=zoneId)
    milight.setSaturation(saturation=0, zoneId=zoneId)
    milight.setBrightness(brightness=100, zoneId=zoneId)
    val_threshold = 0.05
    is_off = False
    last_hue = 0
    last_sat = 0
    last_val = 0
    sent = 0
    while True:
        hue, saturation, val = colorsys.rgb_to_hsv(*_get_average(connection))
        # hue, val, saturation = colorsys.rgb_to_hls(*_get_average())
        if (abs(hue - last_hue) > 0.05
            # or abs(saturation - last_sat) > 0.2 or
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

            milight.setColor(color=round(hue * 255), zoneId=zoneId) # Probs needs more work.
            # milight.setBrightness(brightness=100 - (val * 100), zoneId=4) # Probs needs more work.
            max_sat = 35
            milight.setSaturation(saturation=max_sat - (saturation * max_sat), zoneId=zoneId) # Probs needs more work.
            sent += 1
            print("sending", sent)
            time.sleep(delay)
        time.sleep(delay)


if __name__ == "__main__":

    _send_udp()