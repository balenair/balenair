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
