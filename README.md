# balena-iaq
Indoor air quality device with a matrix LED display driven by a Raspberry Pi 3A+ and two sensors.

![](https://raw.githubusercontent.com/balena-io-playground/balena-iaq/master/images/unit1.jpg)

## Description
The IAQ device uses a CO2 and particulate sensor to generate an indoor air quality score which it displays using an LED matrix on the front of the unit. The easy to remember score ranges from 0 (best air quality) to 99 (hazardous air quality).

The LED display changes color based on the score as follows:
| Score range | Description | LED display color | 
| ------------ | ----------- | ----------- |
| 0 - 49 | Good air quality | green |
| 50 - 74 | Moderate air quality | orange |
| 75 - 99 | Hazardous air quality | red |

We've included STL files so you can print and assemble your own custom case!

## Parts list
2x [Adafruit Bicolor LED Square Pixel Matrix with I2C Backpack](https://www.adafruit.com/product/902)

1x [Adafruit PMSA003I Air Quality Breakout](https://www.adafruit.com/product/4632)

1x [SCD-40 - True CO2, Temperature and Humidity Sensor](https://www.adafruit.com/product/5187)

2x [STEMMA QT / Qwiic JST SH 4-pin Cable - 100mm Long](https://www.adafruit.com/product/4210)

3x [STEMMA QT / Qwiic JST SH 4-pin Cable with Premium Female Sockets - 150mm Long](https://www.adafruit.com/product/4397)

1x [Raspberry Pi 3 Model A+](https://www.raspberrypi.org/products/raspberry-pi-3-model-a-plus/)

1x [SparkFun Qwiic Multiport](https://www.adafruit.com/product/4861) also available [here](https://www.sparkfun.com/products/18012)

## Assembly
The device itself requires no soldering, however the LED pixel matrix does need to be soldered to the I2C backpack as described [here](https://learn.adafruit.com/adafruit-led-backpack/bi-color-8x8-matrix-assembly). (You'll also need to change the I2C address of one of the LED matrix units to 0x71 by soldering together the A0 pads on the back.) All of the components that need to be wired together use I2C, so simply connect everything using the Qwiic multiport and the recommended cables. The two sensors can be daisy-chained, while the two LED backpacks only have headers, so they will need to use the cables with female header sockets on one end. Finally, connect the multiport to the Pi using a similar Qwiic to female header cable. See the diagram below:

![](https://raw.githubusercontent.com/balena-io-playground/balena-iaq/master/images/wiring.png)


## Software

## Usage


## Custom case
The custom case consists of four pieces that can be printed using a standard consumer 3D printer. The files for printing these pieces are in the `stl` folder. They are named as follows:

![](https://raw.githubusercontent.com/balena-io-playground/balena-iaq/master/images/case.png)

### Front
The front panel holds the LED/backpack assemblies. Each assembly slides onto a set of four posts and should be pushed down as far as possible until they rest on the larger diameter section of the posts. The backpack that is set to the 0x71 address by the solder pad blob should be on the right when looking at the back of the face plate. Use a hot soldering iron tip to melt the smaller part of the post to keep the displays in place. The angled headers should face upwards. TIP: attach the female headers before inserting the displays onto the posts.
![](https://raw.githubusercontent.com/balena-io-playground/balena-iaq/master/images/case_front.png)

### Pi Ring
The `pi_ring` holds the Raspberry Pi 3A+ in place. Use four #2-56 pan head screws 1/4" to 5/16" long to mount the Pi in the provided holes. A longer screw will go through the pi_ring so a nut could be added to the other side. 

![](https://raw.githubusercontent.com/balena-io-playground/balena-iaq/master/images/case_pi.png)

### Insulate sense
The `insulate_sense` piece is used to insulate the sensor area from the heat of the Pi. There are mounting holes for both sensors. The bottom of the particulate sensor "sits" on a small shelf. TIP: Tape the blue part of the particulate sensor to the circuit board with a small amount of electrical tape to keep it from sliding around. (Make sure not to cover any of the venting holes on the right of the sensor though!) 
![](https://raw.githubusercontent.com/balena-io-playground/balena-iaq/master/images/case_insulate.png)

There is a small opening at the bottom of this piece to feed the Qwiic sensor cable through to the other side. The side opposite the sensors has a hole to attach the Qwiic multiport connector with a #2-56 1/2" pan head screw and nut.
![](https://raw.githubusercontent.com/balena-io-playground/balena-iaq/master/images/case_insulate_back.png)
### Back
All four pieces are held together by inserting four M3 x 40mm hex socket head screws through the back piece and attaching to the screw holes in the front piece. These screws should not thread into any piece other than the front - they should move freely until they hit the holes in the front. You may need to start the threading on the front piece by inserting a small wood screw and rotating it a few turns.
