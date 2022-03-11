# Import the required libraries
import threading
from functools import partial
from tkinter import *
import pystray
from pystray import MenuItem as item
from PIL import Image

class trayIcon:

    def __init__(self):
        self.active = True
        self.offico = Image.open("off.ico") 
        self.onico = Image.open("on.ico") 

    # Create an instance of tkinter frame or window

    # Define a function for quit the window
    def off(self, *args):
        self.active = False
        self.icon.icon = self.offico

    # Define a function to show the window again
    def on(self, *args):
        self.active = True
        self.icon.icon = self.onico

    def toggle(self, *args):
        if self.active:
            self.off(args)
        else:
            self.on(args)

    def run(self):
    # Hide the window and show on the system taskbar
        image=Image.open("on.ico")
        menu=(
            item('On', partial(self.on, self)),
            item('Off', partial(self.off, self)),
            item('Toggle', partial(self.toggle, self), default=True)
        )

        self.icon=pystray.Icon(
            "name",
            image, "Use LIFX switch", menu,
            doubleclick = partial(self.on, self)
        )
        self.icon.run()

def threaded_function(instance):
    instance.run()

def StartIcon():
    instance = trayIcon()
    thread = threading.Thread(target = threaded_function, args=(instance,))
    thread.start()
    return instance