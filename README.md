# What is this?
This repository allows users to synchronise their compatible device to their [Prismatik](https://github.com/psieg/Lightpack) powered PC backlight!


# Installation
Firstly, a working [Prismatik](https://github.com/psieg/Lightpack) installation is required.

A Prismatik addon is installed by copying a folder to `~\Prismatik\Plugins`. Prismatik will run the addon by reading the `.ini` file with the same
as the directory. e.g. a folder called `Razer-Addon` with a file `Razer-Addon.ini`.

In this repository there are several `.ini` files because this repository can be used with several different devices,
and the device used by Prismatik is based on the directory name. 

Therefore to clone this repository, first navigate to `~Prismatik\plugs`, then: 

## Razer
`git clone <url> Razer-Addon`
## Lifx
`git clone <url> Lifx-Addon`
## OpenRGB
`git clone <url> OpenRGB-Addon`
## Milight
`git clone <url> Milight-Addon`


# Attributions
This repository contains `.ico` files for turning this addon off and on via the system tray.
off icon: https://www.iconfinder.com/icons/2205230/botton_left_off_on_icon
on icon: https://www.iconfinder.com/icons/2205232/botton_off_on_right_icon 
