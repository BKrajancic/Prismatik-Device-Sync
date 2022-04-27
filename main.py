import argparse
import time
import json
from typing import KeysView
from LifxSink import LifxSink
from PrismatikSource import PrismatikSource
from RazerSink import RazerSink
from ThresholdSink import ThresholdSink
from MilightSink import MilightSink 

SINKS = {
    "razer": RazerSink, 
    "lifx": LifxSink,
    "milight": MilightSink
}

def _main():
    with open("config.json", "r") as f:
        config = json.load(f)

    use_icon = config["UseIcon"]
    if use_icon:
        from icon import StartIcon
        icon = StartIcon()

    delay = 1 / config["RefreshRate"]
    source = PrismatikSource()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--type",
        choices= SINKS.keys(),
        help="Type of device to sync")
    args = parser.parse_args()

    sink = SINKS[args.type]
    if config["UseThreshold"]:
        sink = ThresholdSink(sink())

    while True:
        if use_icon and not icon.active:
            continue

        if source.is_running():
            hsv = source.get_hsv()
            sink.send(*hsv)

        time.sleep(delay)

if __name__ == "__main__":
    _main()