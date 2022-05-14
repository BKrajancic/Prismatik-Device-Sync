from HSVSink import HSVSink

class BoosterSink(HSVSink):
    def __init__(self,
                 HSVSink: HSVSink,
                 saturation_boost: float,
                 value_boost: float):
        self._saturation_boost = saturation_boost
        self._value_boost = value_boost
        self._HSVSink = HSVSink 

    def send(self, hue: int, saturation: int, value: int) -> None:
        self._HSVSink.send(
            hue,
            min(1.0, saturation * self._saturation_boost),
            min(1.0, value * self._value_boost)
        )