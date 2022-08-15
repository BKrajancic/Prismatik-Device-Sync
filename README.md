# What is this?
This repository allows users to synchronise compatible devices to a
[Prismatik](https://github.com/psieg/Lightpack) powered PC backlight!

# Device compatibility
The following devices can be used with this addon:

  * [OpenRGB](https://openrgb.org/)
  * [LIFX](https://www.lifx.com/)
  * [Milight/LimitlessLED](https://www.milight.com/)
  * [Razer](https://www.razer.com)

# Installation
Firstly, a working [Prismatik](https://github.com/psieg/Lightpack)
installation is required.

A Prismatik addon is installed by copying a folder to `~/Prismatik/Plugins`.
Prismatik will run the addon by reading the `.ini` file with the same
as the directory. e.g. a folder called `Razer-Addon` with a
file `Razer-Addon.ini`.

In this repository there are several `.ini` files because this repository can
be used with several different devices. This addon can control multiple devices
by being installed several times.

Therefore to install this addon, copy this repository to the plugins folder,
then rename the folder to match the device name. This can be done in two ways:

## Installation using Git
If you have Git installed, open the aforementioned directory using the command
line, then run one of the following commands:

### Razer
`git clone <url> Razer-Addon`
### Lifx
`git clone <url> Lifx-Addon`
### OpenRGB
`git clone <url> OpenRGB-Addon`
### Milight
`git clone <url> Milight-Addon`

## Installation without Git
If you do not have Git installed, install this addon by doing the following:

  1. Download this repository as a `.zip` file, 
  2. Extract it to `~/Prismatik/Plugins`
  3. Rename the folder to match the device to use
     * For Razer: Razer-Addon
     * For Lifx: Lifx-Addon
     * For OpenRGB: OpenRGB-Addon
     * For Milight: Milight-Addon

## Installing Python
[Python](https://www.python.org/downloads/) is used to run the addon, and 
needs to be installed. It also needs accessible in the system path
(typing `python` in the command prompt must open it).

Once python is installed, navigate to the addon directory. Open the command
prompt and type the following:

`python -m pip install -r requirements.txt`

This will install dependencies for the project.

## Enabling connection
In Prismatik, in the 'Expert' section, select "Enable Server."

# Attributions
This repository contains `.ico` files for turning this addon off and on via
the system tray.
  * Off icon: https://www.iconfinder.com/icons/2205230/botton_left_off_on_icon
  * On icon: https://www.iconfinder.com/icons/2205232/botton_off_on_right_icon

# Configuration
In this directory there are several `.json` files that can be edited to to
configure this addon. They are as follows:

## PrismatikConfig.json
This addon works by taking the average of each individual LED in the
backlight. Editing PrismatikConfig allows for controlling which LEDS are
considered.
  * LedStart is the index of the first LED to consider (counting begins from
  0). 
  * LedEnd is the index of the last LED to consider. 
This is useful in cases where the device is situated in a place near an edge,
for instance if your smart light is on the left of the monitor.

### How none works:
  * If LedStart and LedEnd are both `none`, then all LEDs are considered.
  * If only LedStart is `none` then all leds until `LedEnd` are considered.
  * If only LedEnd is `none` then all leds from `LedStart` are considered.

## Config.json
### RefreshRate
How many times per second to update the lights. 

Higher values are more expensive in regards to: computation and network usage
(if this is an online device).

However, lower values can lead to the devices looking different than the PC
backlight.

### UseIcon
If an icon should be added to the tray that allows turning the device on and
off.

### UseThreshold
Instead of sending data to devices x amount of times per second, only send a
new color if it has significantly changed.

### SaturationBoost
Prior to sending the HSV value to the device, the saturation is multiplied by
this value. This means that devices will have stronger colours and less likely
to be white. This is great for some devices (such as RGB mousemats). 

### ValueBoost
Prior to sending the HSV value to the device, the value is multiplied by this
value. This allows for the brightness to be made stronger or weaker.

### SaturationMin
Prior to sending the HSV value to the device, if the saturation percentage is
lower than this value, then the decide is made pure white.

### ValueMin_Off
After calculating the brightness to send to the device, if the brightness to
send is lower than this percentage of the maximum value (0.1 is 10%), the
device will turn off.

### ValueMin_On
After calculating the brightness to send to the device,  brightness to send is
higher than this percentage of the maximum value (0.2 is 20%), and the device
is off, the device will turn back on. Having this value higher than
`ValueMin_Off` avoids flickering if the brightness hovers around that value,
it's also more cinematic as the lights will only turn back on following the
darker scene having completed.

## milightConfig.json
There are 3 parameters. 
1. The IP address of the Milight hub.
2. The port to use (8899 is default).
3. The zone number to use.

## lifxConfig.json
There are two parameters, which is the IP address and Mac Address of the
lightbulb. If these are the empty string, the addon will attempt to
automatically find the LIFX bulb. If not, this allows for selecting which
light to control with the addon. 

Including the IP Address and Mac Address is more reliable.
