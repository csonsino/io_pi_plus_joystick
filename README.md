# io\_pi\_plus\_joystick

Runs a python-uinput based joystick from IO Pi Plus i2c inputs

This project allows an AB Electronics IO Pi Plus Raspberry Pi expansion board (https://www.abelectronics.co.uk/p/54/IO-Pi-Plus) to be used to drive a python-uinput joystick.

The code currently supports a 1-Player and 2-Player joystick, but could easily be expanded to include more joysticks.  The code currently uses a polling mechanism (see the Wishlist), and instead of using a single process with round-robin polling for all joysticks, each joystick runs as a separate process.  The thought is that a multiprocessor device could potentially handle the polling in parallel, thereby eliminating the round-robin delay for button processing on multiple joysticks.  This might be a completely flawed thought process and for all I know it runs serially. 

Refer to io\_pi\_plus\_joystick/input\_def.py for the IO Pi Plus pin - to - uinput joystick button mappings.

# Cloning

This project uses a submodule link to the AB Electronics UK IO Pi Python Library.  To clone this project and the necessary submodule(s), use:

`
git clone --recursive https://github.com/csonsino/io_pi_plus_joystick.git
`

If you already cloned this repo without the "--recursive" argument, you can initialize the submodule(s) by running:

`
git submodule init
`

`
git submodule update
`

# Dependencies

## AB Electronics UK IO Pi Python Library Dependencies

**python-smbus**

For Python 2.7:

`
sudo apt-get install python-smbus
`

For Python 3.4:

`
sudo apt-get install python3-smbus
`

**I2C support enabled**

`
sudo raspi-config
`

Select "Interfacing Options" -> "Enable I2C"

## io\_pi\_plus\_joystick Dependencies

**python-uinput**

`
sudo apt-get install python-pip
`

`
sudo pip install python-uinput
`

Start the uinput kernel module:

`
sudo modprobe uinput
`

Optionally, add/create a modules.conf to autoload the uinput kernel module on boot:

`
sudo nano /etc/modules-load.d/modules.conf
`

Add the line:

`
uinput
`

Save the file and exit

# Usage
To manually run a joystick:

- Use the run_joystick.sh script, supplying a "-p 1" argument for the Player 1 joystick, or a "-p 2" argument for the Player 2 joystick:

 `
 cd <io_pi_plus_joystick_dir>
 `
 
 `
 ./run_joystick.sh -p 1
 `

- Run the python module directly:

 `
 cd <io_pi_plus_joystick_dir>
 `
 
 ``
 export PYTHONPATH=`pwd`:`pwd`/ABElectronics_Python_Libraries/IOPi:`pwd`/io_pi_plus_joystick
 ``
 
 `
 sudo python -m io_pi_plus_joystick.io_pi_plus_joystick -p <1_or_2>
 `

To autoload a joystick using systemd, copy the included script(s) into the /lib/systemd/system/ directory:

 **Note - The scripts assume that you cloned this repository into /opt, if you cloned it into another location, you MUST update the .service scripts accordingly!**

 `
 cd /opt/io_pi_plus_joystick
 `
 
 `
 sudo cp ./systemd/io_pi_plus_joystick_1.service /lib/systemd/system/
 `
 
 `
 sudo cp ./systemd/io_pi_plus_joystick_2.service /lib/systemd/system/
 `
 
 Start the service:
 
 `
 sudo systemctl start io_pi_plus_joystick_1.service
 `
 
 `
 sudo systemctl start io_pi_plus_joystick_2.service
 `
 
 Enable the service on boot:
 
 `
 sudo systemctl enable io_pi_plus_joystick_1.service
 `
 
 `
 sudo systemctl enable io_pi_plus_joystick_2.service
 `

# Testing

The easiest way to test the functionality of your joystick and this code is to use jstest:

Install the joystick tool kit:

`
sudo apt-get install joystick
`

Run jstest

For Player 1 Joystick, typically /dev/input/js0:

`
jstest /dev/input/js0
`

For Player 2 Joystick, typically /dev/input/js1:

`
jstest /dev/input/js1
`

# Wishlist

Ideally the joystick code should operate on an interrupt basis instead of the polling mechanism.  Last I tried, I didn't have much luck using interrupts with the AB Electronics IO Pi Python library (the callbacks seemed to lock up with simultaneous button presses).
