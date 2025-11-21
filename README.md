# Content Aware Auto Brightness

A simple Python script to change brightness based on the content on your screen.

Currently for GNU+Linux with X11 graphic enviroment, might work for Windows and MacOs

## To Install
* Clone this repository.
* Run `pip install -r requirements.txt`.
* Run `python3 main.py <smooth> <min_brightness> <max_brightness> [verbose]`

arguments:
```
smooth: 'true' or 'false'
min_brightness: 0-100
max_brightness: 0-100
verbose: 'true' or 'false' (optional, default: 'true')
```
* example: `python main.py false 30 100 false` 

## For Linux Users
* This uses [xrandr](https://www.commandlinux.com/man-page/man1/xrandr.1.html) for brightness control.

## For MacOS Users
* This uses [brightness](https://github.com/nriley/brightness) for brightness control.
* To install brightness:
`git clone https://github.com/nriley/brightness.git && cd brightness && make && sudo make install`