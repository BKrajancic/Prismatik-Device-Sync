import time
from LifxSink import LifxSink
from PrismatikSource import PrismatikSource
from ThresholdSink import ThresholdSink


def _main():
    useIcon = False
    if useIcon:
        from icon import StartIcon
        icon = StartIcon()

    delay = 1 / 60
    sinks = [ThresholdSink(LifxSink())]
    source = PrismatikSource()

    while True:
        if useIcon:
            if not icon.active:
                continue

        if source.is_running():
            hsv = source.get_hsv()
            for sink in sinks:
                sink.send(*hsv)


        time.sleep(delay)

if __name__ == "__main__":
    _main()