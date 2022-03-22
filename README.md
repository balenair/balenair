![The IAQ](https://raw.githubusercontent.com/balena-io-playground/balena-iaq/master/images/iaq-device-m1.png)

**An attractive device you can easily build that measures the quality of your indoor air and provides readable feedback on an integrated LED display and a web dashboard.**

## Highlights

- **Works with multiple sensors**: Choose among CO2, particulate matter, and VOC sensors based on your needs and budget.
- **Multiple display options**: Choose either a bi-color LED matrix or a multi-color 8 segment LED bargraph.
- **Your data stays local**: Your data remains your own. It is stored locally and can be accessed by a built-in secure VPN.
- **Onboard web dashboard**: Provides real time gauges and measurement history over time for detecting trends. 

![Dashboard](https://raw.githubusercontent.com/balena-io-playground/balena-iaq/master/images/dashboard.png)

## Description and use
The IAQ device uses a combination of CO2, VOC, and particulate sensors to generate an indoor air quality score.  The standard IAQ device displays the score using an LED matrix on the front of the unit. The easy-to-remember score ranges from 0 (best air quality) to 99 (hazardous air quality). Other simpler display options use one or more LEDs to show a color based on the score. The IAQ is powered by a Raspberry Pi. (See here for supported versions.) The IAQ can calculate and display an air quality score without internet access, but does require internet access for initial software download and to view your dashboard outside your internal network.

The LED display changes color based on the score as follows:
| Score range | Description | LED display color | 
| ------------ | ----------- | ----------- |
| 0 - 49 | Good air quality | green |
| 50 - 74 | Moderate air quality | orange |
| 75 - 99 | Unhealthy air quality | red |

### The sensors
The project consists of up to three sensors but only one is required. You can choose any or all depending on your needs and budget. The air quality score is comprised of a combination of readings from the available sensors. 

- Particulate sensors for smoke, dust, pollen and other tiny particles
- CO2 sensor for exhaled breath and burning fossil fuels
- Volatile Organic Compound (VOC) sensor for gasses emitted by solid and liquid products
- Temperature and humidity environmental sensors

Since all of the sensors utilize an I2C Qwiic connector, no soldering is required. See the parts list in the documentation for more details on cost and availability of these sensors.

### The display

![IAQ displays](https://raw.githubusercontent.com/balena-io-playground/balena-iaq/new-docs/docs/images/displays.png)

The standard display uses two 1.2" Bi-color 8x8 LED Matrix displays that cost about $16 each ($32 total). This display provides visual feedback of the air quality score and changes color as the score increases. A less costly option utilizes an eight segment multi-color LED bargraph that displays the air quality score as a horizontal graph that also changes color as the score changes. 

The standard matrix display requires some soldering to build. The bargraph LED version can be built without any soldering.

See the parts list in the Getting Started guide for more details on cost and availability of the display parts.

### The case

We provide STL files so you can use your 3D printer to print a beautiful case for the IAQ. Don't have a 3D printer? Use this link to order the case parts from a local service bureau.

The case consists of four interlocking layers that are held together by four M3 x 40mm hex socket head screws. The case accomodates any or all of the supported sensors, two different Raspberry Pis, as well as any of the display options. (A printable bracket may be required)

See the documentation for more information about printing and assembly of the case.

## Documentation

Head over to our docs for detailed parts lists, options, building, installation and usage instructions, customization options and more!

## Getting Help

If you're having any problem, please [raise an issue](https://github.com/balena-io-playground/balena-iaq/issues/new) on GitHub and we will be happy to help.

## Contributing

Do you want to help make IAQ better? Take a look at our [Contributing Guide](https://sound.balenalabs.io/contributing). Hope to see you around!

## License

IAQ is free software, and may be redistributed under the terms specified in the license.
