#!/usr/bin/python
#
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

"""Runs a python-uinput based joystick from IO Pi Plus i2c inputs"""

import argparse

from ABElectronics_Python_Libraries.IOPi.IOPi import IOPi
import time
import os
import uinput

# input_def contains the mapping between i2c pin number and button constant
import input_def

__author__ = "Carey Sonsino"
__copyright__ = "Copyright 2017"
__credits__ = ["Carey Sonsino", "AB Electronics UK", "Chris Swan"]
__license__ = "GPL"
__version__ = "2"
__maintainer__ = "Carey Sonsino"
__email__ = "csonsino@gmail.com"
__status__ = "Development"

# all possible events
events = (
    uinput.ABS_X + (input_def.JOYSTICK_LEFT_VALUE, input_def.JOYSTICK_RIGHT_VALUE, 0, 0),
    uinput.ABS_Y + (input_def.JOYSTICK_UP_VALUE, input_def.JOYSTICK_DOWN_VALUE, 0, 0),
    uinput.BTN_THUMBL,
    uinput.BTN_THUMBR,
    uinput.BTN_A,
    uinput.BTN_B,
    uinput.BTN_X,
    uinput.BTN_Y,
    # uinput.BTN_LEFT,   # DON'T USE THIS - It breaks gamepad detection
    # uinput.BTN_RIGHT,  # DON'T USE THIS - It breaks gamepad detection
    uinput.BTN_C,
    uinput.BTN_Z,
    uinput.BTN_START,
    uinput.BTN_BACK,
    uinput.BTN_FORWARD,
    uinput.BTN_SELECT,
    )

device = uinput.Device(events)

_pins_inverted = input_def.BUTTON_PRESS_RAW_VALUE != input_def.BUTTON_PRESS_RAW_VALUE_DEFAULT


class JoystickButton:
    """
    This class represents a joystick button
    """

    def __init__(self,
                 pin,
                 emit=None,
                 emit_press_value=input_def.BUTTON_PRESS_EMIT_VALUE,
                 emit_release_value=input_def.BUTTON_RELEASE_EMIT_VALUE):
        self.pressed = False
        self.i2c_pin = pin
        self.emit = emit
        self.emit_press_value = emit_press_value
        self.emit_release_value = emit_release_value

    @staticmethod
    def _pin_pressed(pin_val):
        """
        Normalizes pin values for possibly inverted pins
        :param pin_val:
        :return:
        """
        if _pins_inverted:
            return pin_val == 1
        else:
            return pin_val == 0

    def check_button(self, bus):
        """
        Checks if this button is pressed, and emits the the press or release event if the state has changed
        :param bus: IOPi bus to check
        :return: True if this button is pressed, False otherwise
        """
        pin_val = bus.read_pin(self.i2c_pin)
        pin_pressed = self._pin_pressed(pin_val)

        if input_def.DEBUG_JOYSTICK:
            print 'Pin  ' + str(self.i2c_pin) + ': ' + str(pin_val)

        if pin_pressed and not self.pressed:
            self.pressed = True
            if self.emit is not None and self.emit_press_value is not None:
                device.emit(self.emit, self.emit_press_value)
        elif not pin_pressed and self.pressed:
            self.pressed = False
            if self.emit is not None and self.emit_release_value is not None:
                device.emit(self.emit, self.emit_release_value)

        return self.pressed


class JoystickInput:
    """
    This class represents a single player's input (directional joystick and buttons)
    """

    _bus_joystick_left = JoystickButton(input_def.JOYSTICK_LEFT,
                                        uinput.ABS_X, input_def.JOYSTICK_LEFT_VALUE, input_def.JOYSTICK_NEUTRAL_VALUE)
    _bus_joystick_right = JoystickButton(input_def.JOYSTICK_RIGHT,
                                         uinput.ABS_X, input_def.JOYSTICK_RIGHT_VALUE, input_def.JOYSTICK_NEUTRAL_VALUE)
    _bus_joystick_up = JoystickButton(input_def.JOYSTICK_UP,
                                      uinput.ABS_Y, input_def.JOYSTICK_UP_VALUE, input_def.JOYSTICK_NEUTRAL_VALUE)
    _bus_joystick_down = JoystickButton(input_def.JOYSTICK_DOWN,
                                        uinput.ABS_Y, input_def.JOYSTICK_DOWN_VALUE, input_def.JOYSTICK_NEUTRAL_VALUE)
    # NOTE - Buttons have default values for press/release
    _bus_button_7 = JoystickButton(input_def.BUTTON_1, uinput.BTN_THUMBL)
    _bus_button_8 = JoystickButton(input_def.BUTTON_2, uinput.BTN_THUMBR)
    _bus_button_1 = JoystickButton(input_def.BUTTON_3, uinput.BTN_A)
    _bus_button_2 = JoystickButton(input_def.BUTTON_4, uinput.BTN_B)
    _bus_button_3 = JoystickButton(input_def.BUTTON_5, uinput.BTN_C)
    _bus_button_4 = JoystickButton(input_def.BUTTON_6, uinput.BTN_X)
    _bus_button_5 = JoystickButton(input_def.BUTTON_7, uinput.BTN_Y)
    _bus_button_6 = JoystickButton(input_def.BUTTON_8, uinput.BTN_Z)

    _bus_button_start = JoystickButton(input_def.BUTTON_PLAYER_START, uinput.BTN_START)

    __bus_buttons = None

    _bus_address = None
    _bus = None

    def __init__(self, bus_address=input_def.BUS_1_ADDRESS):
        """
        Initializes this JoystickInput
        :param bus_address: IOPi bus address
        """
        self._bus_address = bus_address

        self._bus = IOPi(self._bus_address)

        # We are using the pins in read only mode
        self._bus.set_port_direction(0, 0xFF)
        self._bus.set_port_direction(1, 0xFF)

        # Enable the internal pull-up resistors
        self._bus.set_port_pullups(0, 0xFF)
        self._bus.set_port_pullups(1, 0xFF)

        if _pins_inverted:
            # invert the ports so that presses register as 1 instead of 0
            self._bus.invert_port(0, 0xFF)
            self._bus.invert_port(1, 0xFF)

    def _get_bus_buttons(self):
        """
        Gets the list of buttons for this bus
        :return: List of JoystickButtons
        """
        if self.__bus_buttons is None:
            self.__bus_buttons = [
                self._bus_joystick_left,
                self._bus_joystick_right,
                self._bus_joystick_up,
                self._bus_joystick_down,
                self._bus_button_1,
                self._bus_button_2,
                self._bus_button_3,
                self._bus_button_4,
                self._bus_button_5,
                self._bus_button_6,
                self._bus_button_7,
                self._bus_button_8,
                self._bus_button_start,
            ]
        return self.__bus_buttons

    def _post_process_buttons(self):
        """
        Allows the opportunity to perform post processing on buttons
        :return:
        """
        pass

    def run_joystick(self):
        """
        Runs the polling loop for input detection
        :return:
        """
        # Center joystick
        # syn=False to emit an "atomic" event.
        device.emit(uinput.ABS_X, input_def.JOYSTICK_NEUTRAL_VALUE, syn=False)
        device.emit(uinput.ABS_Y, input_def.JOYSTICK_NEUTRAL_VALUE)

        while True:
            if input_def.DEBUG_JOYSTICK:
                # clear the console
                os.system('clear')

            for button in self._get_bus_buttons():
                button.check_button(self._bus)

            self._post_process_buttons()

            # wait 0.? seconds before reading the pins again
            time.sleep(input_def.BUTTON_POLL_S)


class Player1Joystick(JoystickInput):
    """
    Player 1 Joystick / Button Input
    """
    __bus_buttons = None

    _bus_button_back = JoystickButton(input_def.BUTTON_BUS1_BACK, uinput.BTN_BACK)
    _bus_button_coin = JoystickButton(input_def.BUTTON_BUS1_COIN, uinput.BTN_FORWARD)
    _bus_button_white = JoystickButton(input_def.BUTTON_BUS1_WHITE, uinput.BTN_SELECT)

    def __init__(self):
        """
        Initializes the Player 1 Joystick Input
        """
        JoystickInput.__init__(self, input_def.BUS_1_ADDRESS)

    def _get_bus_buttons(self):
        """
        Gets the list of buttons for this Joystick Input
        :return: List of JoystickButtons
        """
        if self.__bus_buttons is None:
            # Start with the common set of buttons
            # self.__bus_buttons = super(Player1Joystick, self)._get_bus_buttons()
            self.__bus_buttons = JoystickInput._get_bus_buttons(self)

            # Add the bus specific buttons

            self.__bus_buttons.extend([
                self._bus_button_back,
                self._bus_button_coin,
                self._bus_button_white,
            ])
        return self.__bus_buttons


class Player2Joystick(JoystickInput):
    __bus_buttons = None

    _bus_button_black = JoystickButton(input_def.BUTTON_BUS2_BLACK, uinput.BTN_SELECT)

    # NOTE - This button does not emit a joystick value, we're using it to power down
    _bus_button_power = JoystickButton(input_def.BUTTON_BUS2_POWER, emit=None)

    def __init__(self):
        """
        Initializes the Player 2 Joystick Input
        """
        JoystickInput.__init__(self, input_def.BUS_2_ADDRESS)

    def _get_bus_buttons(self):
        """
        Gets the list of buttons for this Joystick Input
        :return: List of JoystickButtons
        """
        if self.__bus_buttons is None:
            # Start with the common set of buttons
            # self.__bus_buttons = super(Player2Joystick, self)._get_bus_buttons()
            self.__bus_buttons = JoystickInput._get_bus_buttons(self)

            # Add the bus specific buttons

            self.__bus_buttons.extend([
                self._bus_button_black,
                self._bus_button_power,
            ])
        return self.__bus_buttons

    def _post_process_buttons(self):
        """
        Post processing for the buttons
        :return:
        """
        JoystickInput._post_process_buttons(self)
        if self._bus_button_power.pressed:
            print "Shutdown Requested by power button..."
            input_def.power_off()


if __name__ == "__main__":
    """
    Runs a python-uinput based joystick from IO Pi Plus i2c inputs
    """
    parser = argparse.ArgumentParser(description='Runs a python-uinput based joystick from IO Pi Plus i2c inputs')
    parser.add_argument('-p', '--player', metavar="player", type=int, choices=range(1, 3), required=True,
                        help='Player number of the Joystick (1 or 2)')

    args = parser.parse_args()
    if input_def.DEBUG_JOYSTICK:
        print "args: " + str(args)
        print "args.player: " + str(args.player)

    joystick = None
    if args.player is None:
        print "Error: Player number is None"
    elif args.player == 1:
        joystick = Player1Joystick()
    elif args.player == 2:
        joystick = Player2Joystick()
    else:
        print "Invalid 'player' argument: " + str(args['player'])

    if joystick is not None:
        joystick.run_joystick()
