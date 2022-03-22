# Hardware setup

Once you have all of your parts gathered, it's a good idea to walk through this assembly guide to get familiar with how everything gets connected together. Even if you will be using the 3D printed case, you may want to connect everything together and install the software before placing everything in the case. All of the connections are modular so it's easy to disconnect all of the parts and re-cobbect them again later inside the case. Make sure your Pi is powered off during the hardware setup!

## Connecting the sensors

All of the sensors utilize the I2C data bus and contain Qwiic connectors, so they can all be connected together rather easily. 

Start by connecting the female jumpers on one end of the "150 mm Qwiic to 4 pin female cables" to the Raspberry Pi. Note the pin assignments based on the wire color using the diagram below:

![](https://raw.githubusercontent.com/balena-io-playground/balena-iaq/new-docs/docs/images/hardware-setup-pi-connect.png)

- The red wire goes to pin 1 (3v)
- The blue wire goes to pin 3 (SDA)
- The yellow wire goes to pin 5 (SCL)
- The black wire goes to pin 9 (Gnd)

The connector at the other end of the cable connects to any one of the four ports on the multiport connector. Now connect one end of the "200mm QT to QT cable" to any of the three remaining empty ports on the multiport connector. This is the long cable that will be used to connect to the first sensor since when mounted in the case, the multiport will be somewhat far from this sensor. The other end of this cable can be connected to the first sensor. When mounted in the case, the first sensor is physically the blue rectangular particulate sensor. However, you can connect the sensors in any order you please. Use the remaining "QT to QT" cables to connect any remaining sensors you may have in a daisy chain fashion as shown below:

![](https://raw.githubusercontent.com/balena-io-playground/balena-iaq/new-docs/docs/images/hardware-setup-sensor-connect.png)

## Connecting the display

### LED matrix assembly

If you're using the two LED matrix boards, you'll first need to solder each LED matrix to its backpack as described [here](https://learn.adafruit.com/adafruit-led-backpack/bi-color-8x8-matrix-assembly). Then solder the four pin male headers to each backpack. If you will be using the standard case, you must use the angled headers as specified in the parts list, not the straight headers included in the backpack kit. Make sure the headers are angled outwards as shown below:

You'll also need to change the I2C address of one of the displays. using [this guide](https://learn.adafruit.com/adafruit-led-backpack/changing-i2c-address), solder together the A0 pads of one display to change its address from 0x70 to 0x71. This will be the left digit when facing the two displays.

Finally, use the two remaining "Qwiic to female jumper" cables to connect the two displays to the two open ports on the multiport connector. The jumper cables connect to the headers as follows:

- The yellow jumper connects to SCL
- The blue jumper connects to SDA
- The black jumper connects to GND
- The red jumper connects to VCC

### LED bargraph display

Connecting this type of display is easy: simply connect one end of a 100mm Qwiic connector to one of the jacks on the LED stick. Connect the other end to a free port in the 4-way Qwiic multiport connector.
