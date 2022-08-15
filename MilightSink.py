import time
import json
from HSVSink import HSVSink

from MilightWifiBridge import MilightWifiBridge

class MilightSink(HSVSink):
    def __init__(self):
        with open("milightConfig.json", "r") as f:
            config = json.load(f)
        self._ip = config["ip"]
        self._port = config["port"]
        self._zoneId = config["zoneId"]
        self._milight = MilightWifiBridge.MilightWifiBridge()
        self._milight.setup(ip=self._ip, port=self._port, timeout_sec=0.50)
        self._is_off = False
        self._reset()

    def _reset(self):
        delay = 0.5
        self._milight.turnOn(zoneId=self._zoneId)
        time.sleep(delay)
        self._milight.setWhiteMode(self._zoneId)
        time.sleep(delay)
        self._milight.setTemperature(100, self._zoneId)
        time.sleep(delay)
        self._milight.setBrightness(brightness=100, zoneId=self._zoneId)
        time.sleep(delay)
        self._milight.setColor(0, self._zoneId)
        time.sleep(delay)
        self._milight.setSaturation(saturation=0, zoneId=self._zoneId)
        time.sleep(delay)
        self._milight.setBrightness(brightness=100, zoneId=self._zoneId)
        self._is_off = False

    def send(self, hue: float, saturation: float, val: float):
        val_threshold = 0.05

        if self._is_off:
            if val > val_threshold:
                self._milight.turnOn(zoneId=self._zoneId)
                self._is_off = False
        elif val < val_threshold:
            self._milight.turnOff(zoneId=self._zoneId)
            self._is_off = True
            return

        saturation_max = 100
        saturation_threshold = 15
        saturation_scaled = saturation * saturation_max
        if saturation_scaled < saturation_threshold:
            self._milight.setWhiteMode(self._zoneId)
        else:
            scaled_hue = hue * 255
            if scaled_hue > 250:
                self._milight.setColor(color=16, zoneId=self._zoneId)
                self._milight.setSaturation(saturation=100 - saturation_scaled, zoneId=self._zoneId)
            else:
                if scaled_hue < 68:
                    scaled_hue += 0x0F
                    scaled_hue %= 0xFF

                self._milight.setColor(color=scaled_hue, zoneId=self._zoneId)
                self._milight.setSaturation(saturation=100 - saturation_scaled, zoneId=self._zoneId)

        self._milight.setBrightness(brightness=val * 100, zoneId=self._zoneId)
