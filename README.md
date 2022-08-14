# What is this?
This repository allows users to synchronise their compatible device to their [Prismatik](https://github.com/psieg/Lightpack) powered PC backlight!

# Device compatibility
The following devices can be used with this addon:

  * [OpenRGB](https://openrgb.org/)
  * [LIFX](https://www.lifx.com/)
  * [Milight/LimitlessLED](https://www.milight.com/)
  * [Razer](https://www.razer.com)


# Installation
Firstly, a working [Prismatik](https://github.com/psieg/Lightpack) installation is required.

A Prismatik addon is installed by copying a folder to `~/Prismatik/Plugins`. Prismatik will run the addon by reading the `.ini` file with the same
as the directory. e.g. a folder called `Razer-Addon` with a file `Razer-Addon.ini`.

In this repository there are several `.ini` files because this repository can be used with several different devices. This addon can control multiple devices by being installed several times.

Therefore to install this addon, copy this repository to the plugins folder, then rename the folder to match the device name. This can be done in two ways:

## Installation using Git
If you have Git installed, open the aforementioned directory using the command line, then run one of the following commands:

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

# Attributions
This repository contains `.ico` files for turning this addon off and on via the system tray.
  * Off icon: https://www.iconfinder.com/icons/2205230/botton_left_off_on_icon
  * On icon: https://www.iconfinder.com/icons/2205232/botton_off_on_right_icon 
