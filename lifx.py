import json
import time
import operator
import os
import socket
from RGBDevice_Lifx import LifxAdapter
from bulb_threshold import BulbThreshold
from utils import (
    _get_average_rgb,
    is_on,
)

def get_connection():
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect(("127.0.0.1", 3636))
    connection.recv(8192)
    return connection

def _main():
    useIcon = False
    if useIcon:
        from icon import StartIcon
        icon = StartIcon()

    connection = get_connection()
    delay = 1 / 60
    gamma = 1.0
    bulb = BulbThreshold(LifxAdapter())

    while True:
        if useIcon:
            if not icon.active:
                continue

        if not is_on(connection):
            continue

        current_set = _get_average_rgb(
            connection, 
            gamma_correction=gamma,
            nth=1
        )

        bulb.send(*current_set)
        time.sleep(delay)

if __name__ == "__main__":
    _main()
