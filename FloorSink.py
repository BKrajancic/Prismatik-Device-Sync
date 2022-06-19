from HSVSink import HSVSink

class FloorSink(HSVSink):
    def __init__(self,
                 HSVSink: HSVSink,
                 saturation_min: float,
                 value_min_off: float,
                 value_min_on: float):
        self._saturation_min = saturation_min
        self._HSVSink = HSVSink 
        self._value_min_on = value_min_on
        self._value_min_off = value_min_off
        self._is_on = True

    def send(self, hue: int, saturation: int, value: int) -> None:
        saturation = (saturation - self._saturation_min) / (1 - self._saturation_min)
        saturation = max(saturation, 0)

        if self._is_on and value <= self._value_min_off:
            value = 0
            self._is_on = False
        elif not self._is_on and value < self._value_min_on:
            value = 0
        
        if not self._is_on and value > 0:
            self._is_on = True

        self._HSVSink.send(hue, saturation, value)