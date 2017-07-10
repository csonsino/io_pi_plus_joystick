# This file is part of io_pi_plus_joystick.  io_pi_plus_joystick is free software:
# you can redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright io_pi_plus_joystick Team Members

"""Contains the input definition mapping for pins to buttons"""

__author__ = "Carey Sonsino"
__copyright__ = "Copyright 2017"
__credits__ = ["Carey Sonsino", "AB Electronics UK", "Chris Swan"]
__license__ = "GPL"
__version__ = "2"
__maintainer__ = "Carey Sonsino"
__email__ = "csonsino@gmail.com"
__status__ = "Development"

# Set to True to print detected inputs
# DEBUG_JOYSTICK = True
DEBUG_JOYSTICK = False

# This is the number of seconds between polling the bus
BUTTON_POLL_S = 0.01

# These are controlled by the jumpers on the IO Pi Plus board
BUS_1_ADDRESS = 0x20
BUS_2_ADDRESS = 0x21

# Joystick values
JOYSTICK_NEUTRAL_VALUE = 128
JOYSTICK_LEFT_VALUE = 0
JOYSTICK_RIGHT_VALUE = 255
JOYSTICK_UP_VALUE = 0
JOYSTICK_DOWN_VALUE = 255

# If the button press value is 1, the pins will need to be inverted
# By default, the button press goes low
BUTTON_PRESS_RAW_VALUE_DEFAULT = 0
BUTTON_PRESS_RAW_VALUE = 0
BUTTON_RELEASE_RAW_VALUE = 1

# DO NOT CHANGE THESE!
# These are the values that the python-uinput module are expecting
BUTTON_PRESS_EMIT_VALUE = 1
BUTTON_RELEASE_EMIT_VALUE = 0

###################
# Common Bus Inputs
###################
JOYSTICK_LEFT = 1
JOYSTICK_RIGHT = 2
JOYSTICK_UP = 3
JOYSTICK_DOWN = 4
BUTTON_1 = 5
BUTTON_2 = 6
BUTTON_3 = 7
BUTTON_4 = 8
BUTTON_5 = 9
BUTTON_6 = 10
BUTTON_7 = 11
BUTTON_8 = 12

# This is the P1/P2 button
BUTTON_PLAYER_START = 13

#######################
# Bus 1 Specific Inputs
#######################
BUTTON_BUS1_BACK = 14
BUTTON_BUS1_COIN = 15
BUTTON_BUS1_WHITE = 16

#######################
# Bus 2 Specific Inputs
#######################
BUTTON_BUS2_BLACK = 14
# BUTTON_BUS2_xxx = 15  # CURRENTLY UNUSED
BUTTON_BUS2_POWER = 16


def power_off():
    """
    Power off the device
    :return:
    """
    command = "/usr/bin/sudo /sbin/poweroff"
    if DEBUG_JOYSTICK:
        # FOR DEBUGGING! - exit only (don't power off)
        command = "/bin/echo 'POWER button pressed!'"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output
