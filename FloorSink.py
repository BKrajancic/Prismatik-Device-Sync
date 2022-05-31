from HSVSink import HSVSink

class FloorSink(HSVSink):
    def __init__(self,
                 HSVSink: HSVSink,
                 saturation_min: float,
                 value_min: float):
        self._saturation_min = saturation_min
        self._value_min = value_min
        self._HSVSink = HSVSink 

    def send(self, hue: int, saturation: int, value: int) -> None:
        if saturation < self._saturation_min:
            saturation = 0
        if value < self._value_min:
            value = 0

        self._HSVSink.send(hue, saturation, value)