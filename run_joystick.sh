#!/bin/sh

export PYTHONPATH=`pwd`:`pwd`/ABElectronics_Python_Libraries/IOPi:`pwd`/io_pi_plus_joystick
sudo python -m io_pi_plus_joystick.io_pi_plus_joystick "$*"

exit 0
