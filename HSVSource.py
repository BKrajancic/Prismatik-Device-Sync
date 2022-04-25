from typing import Tuple

class HSVSource():
    def is_running(self) -> bool:
        raise NotImplementedError()

    def get_hsv(self) -> Tuple[float, float, float]:
        raise NotImplementedError()
