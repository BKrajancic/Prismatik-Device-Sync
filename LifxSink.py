from audioop import mul
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
        self._last_kelvin = 0
        self._saturation_min = 0.20

    def is_on(self, connection: socket.socket) -> bool:
        self.connection.send(str.encode("getstatus\n"))
        data: str = connection.recv(8192).decode().strip()
        return data == "status:on"

    def _saturation_to_kelvin(self, saturation: int):
        return min(1, pow(saturation / self._saturation_min, 2))

    def _hue_to_kelvin(self, hue: int):
        return -abs(0.5 - hue) + 0.5

    def _get_kelvin(self, hue: int, saturation: int, value: int):
        kelvin_val = self._kelvin_range[1]

        hue_multiplier = self._hue_to_kelvin(hue)
        sat_multiplier = self._saturation_to_kelvin(saturation)
        multiplier = hue_multiplier + (1 - sat_multiplier)
        multiplier = max(multiplier, 0)
        multiplier = min(multiplier, 1)

        kelvin_range = self._kelvin_range[1] - self._kelvin_range[0]
        new_kelvin_val = self._kelvin_range[0] + (multiplier * kelvin_range)
        kelvin_val = new_kelvin_val
        self._last_kelvin = round(kelvin_val)
        return self._last_kelvin

    def send(self, hue: int, saturation: int, value: int) -> None:
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
