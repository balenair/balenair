![The IAQ](https://raw.githubusercontent.com/balena-io-playground/balena-iaq/images/iaq-device-m1.png)

**An attractive device you can easily build that measures the quality of your indoor air and provides readable feedback on an integrated LED display and a web dashboard.**

## Highlights

- **Works with multiple sensors**: Choose among CO2, particulate matter, and VOC sensors based on your needs and budget.
- **Multiple display options**: Choose from a tri-color LED matrix, a 12 segment LED bargraph, or a single tri-color LED.
- **Detailed web dashboard**: Provides real time gauges and measurement history over time for detecting trends. 

## Description and use
The IAQ device uses a combination of CO2, VOC, and particulate sensors to generate an indoor air quality score.  The standard IAQ device displays the score using an LED matrix on the front of the unit. The easy-to-remember score ranges from 0 (best air quality) to 99 (hazardous air quality). Other simpler display options use one or more LEDs to show a color based on the score. The IAQ is powered by a Raspberry Pi 3A+ or Zero 2W.

The LED display changes color based on the score as follows:
| Score range | Description | LED display color | 
| ------------ | ----------- | ----------- |
| 0 - 49 | Good air quality | green |
| 50 - 74 | Moderate air quality | orange |
| 75 - 99 | Unhealthy air quality | red |

### The sensors
The project consists of up to three sensors (listed below) but only one is required. You can choose any or all depending on your needs and budget. The air quality score is comprised of the following readings:

| Reading | Description | Sensor Type | good range (0 - 50) | moderate range (51 - 74) | unhealthy range (75 - 99) |
| ------------ | ----------- | ----------- | ----------- | ----------- | ----------- |
| PM2.5 | Smoke, dust, dirt, pollen | PMSA003I | 12 - 34 ug/m3 | 35 - 54 ug/m3 | 55+ ug/m3 |
| PM10 | Dust, smoke, exhaust, tiny particles | PMSA003I | 0 - 53 ug/m3 | 54 - 149 ug/m3 | 150+ ug/m3 |
| CO2 | Exhaled breath and burning fossil fuels | SCD-40 | 400 - 999 PPM | 1000 - 1999 PPM | 2000+ PPM |
| VOC | Gasses emitted by solid and liquid products  | SGP-30 | 0 - 499 PPB | 500 - 999 PPB | 1000+ PPB |

The reading with the highest index is the one that will be displayed. At startup, the device will display a list of the sensors that were detected.

Since all of the sensors utilize the I2C Qwiic connector, no soldering is required. See the parts list in the Getting Started guide for more details on cost and availability of these sensors.

### The display

![IAQ displays](https://raw.githubusercontent.com/balena-io-playground/balena-iaq/images/three-iaq-displays.png)

The standard display uses two 1.2" Bi-color 8x8 LED Matrix displays that cost about $16 each ($32 total). This display provides visual feedback of the air quality score and changes color as the score increases. A less costly option utilizes a 12 segment bi-color LED bargraph that displays the air quality score as a horizontal graph that also changes color as the score increases. The least costly option is a single large bi-color LED that only indicates whether the score is low, moderate, or high.

The standard matrix display and the LED bargraph requires some soldering to build. The single bi-color LED version can be built without any soldering.

See the parts list in the Getting Started guide for more details on cost and availability of the display parts.


### The case

We provide STL files so you can use your 3D printer to print a beautiful case for the IAQ. Don't have a 3D printer? Use this link to order the case parts from a local service bureau.

The case consists of four interlocking layers that are held together by four M3 x 40mm hex socket head screws. The case accomodates any or all of the supported sensors, as well as all of the display options.

See the documentation for more information about printing and assembly of the case.

## Documentation

Head over to our docs for detailed parts lists, options, building, installation and usage instructions, customization options and more!

## Getting Help

If you're having any problem, please [raise an issue](https://github.com/balena-io-playground/balena-iaq/issues/new) on GitHub and we will be happy to help.

## Contributing

Do you want to help make IAQ better? Take a look at our [Contributing Guide](https://sound.balenalabs.io/contributing). Hope to see you around!

## License

IAQ is free software, and may be redistributed under the terms specified in the license.
