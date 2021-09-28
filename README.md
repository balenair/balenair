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

1x [SparkFun Qwiic Multiport](https://www.adafruit.com/product/4861) or [here](https://www.sparkfun.com/products/18012)

## Assembly
The device itself requires no soldering, however the LED pixel matrix does need to be soldered to the I2C backpack as described [here](https://learn.adafruit.com/adafruit-led-backpack/bi-color-8x8-matrix-assembly). 
