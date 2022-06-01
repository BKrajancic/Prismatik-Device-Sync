from HSVSink import HSVSink
import socket
import os
import json
from lifxlan import LifxLAN, Light

def _get_bulb() -> Light:
    lifxlan = LifxLAN()
    configFilepath = "lifxConfig.json"
    if os.path.exists(configFilepath):
        with open(configFilepath, 'r') as f:
            config = json.load(f)[0]
            bulb = Light(config['mac_address'], config['ip_address'])
    else:
        bulb: Light = lifxlan.get_color_lights()[0]
    return bulb


class LifxSink(HSVSink):
    def __init__(self) -> None:
        self.bulb = _get_bulb()
        self._is_on = False
        self.bulb.set_power(True, rapid=True)
        self._kelvin_range = [self.bulb.get_min_kelvin() + 1500, self.bulb.get_max_kelvin()]
        col = self.bulb.get_color()

    def is_on(self, connection: socket.socket) -> bool:
        self.connection.send(str.encode("getstatus\n"))
        data: str = connection.recv(8192).decode().strip()
        return data == "status:on"

    def _get_kelvin(self, hue: int, saturation: int, value: int):
        kelvin_val = self._kelvin_range[1]
        pure_white = saturation < 0.01
        # brown_zone = 0.3
        # if (hue > brown_zone):
        #     return 6500


        if not (pure_white) and hue not in [0.0, 0]:
            kelvin_val = (
                0.5 - (hue - 0.5)
                if hue > 0.5
                else hue
            )

            kelvin_val *= self._kelvin_range[1] - self._kelvin_range[0]
            kelvin_val += self._kelvin_range[0]
        return round(kelvin_val)

    def send(self, hue: int, saturation: int, value: int) -> None:
        # col = self.bulb.get_color()
        max_val = 65535
        current_set = (hue, saturation, value)
        current_set = [round(val * max_val) for val in current_set]
        current_set.append(self._get_kelvin(hue, saturation, value))
        # (5461, 18724, 25700, 3500)
        self.bulb.set_color(current_set, rapid=True)

        if value == 0 and self._is_on:
            self.bulb.set_power(False, rapid=True)
        if value != 0 and not self._is_on:
            self.bulb.set_power(True, rapid=True)
