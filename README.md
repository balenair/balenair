# balena-iaq
Indoor air quality monitoring device with a matrix LED display driven by a Raspberry Pi and one or more sensors.

![](https://raw.githubusercontent.com/balena-io-playground/balena-iaq/master/images/unit2.jpg)

## Description and use
The IAQ device uses a combination of CO2, VOC, and particulate sensors to generate an indoor air quality score which it displays using an LED matrix on the front of the unit. The easy-to-remember score ranges from 0 (best air quality) to 99 (hazardous air quality).

The LED display changes color based on the score as follows:
| Score range | Description | LED display color | 
| ------------ | ----------- | ----------- |
| 0 - 49 | Good air quality | green |
| 50 - 74 | Moderate air quality | orange |
| 75 - 99 | Unhealthy air quality | red |

The project consists of up to three sensors (listed below) but only one is required. You can choose any or all depending on your needs. The air quality score is comprised of the following readings:

| Reading | Description | Sensor Type | good range (0 - 50) | moderate range (51 - 74) | unhealthy range (75 - 99) |
| ------------ | ----------- | ----------- | ----------- | ----------- | ----------- |
| PM2.5 | Smoke, dust, dirt, pollen | PMSA003I | 12 - 34 ug/m3 | 35 - 54 ug/m3 | 55+ ug/m3 |
| PM | Dust, smoke, exhaust, tiny particles | PMSA003I | 0 - 53 ug/m3 | 54 - 149 ug/m3 | 150+ ug/m3 |
| CO2 | Exhaled breath and burning fossil fuels | SCD-40 | 400 - 999 PPM | 1000 - 1999 PPM | 2000+ PPM |
| VOC | Gasses emitted by solid and liquid products  | SGP-30 | 0 - 499 PPB | 500 - 999 PPB | 1000+ PPB |

The reading with the highest index is the one that will be displayed. At startup, the device will display a list of the sensors that were detected.

The device can alternate between displaying the index and the name of the pollutant with the highest reading by setting the device [configuration variable](https://www.balena.io/docs/learn/manage/variables/) `ALERT_MODE`. The defualt value of `0` (or no setting) will never display the pollutant. A value of `1` will only display the pollutant if the index is over the `ALERT_LEVEL` variable, and a value of `2` will always alternate the display with the pollutant name regardless of the index value.


## Parts list
2x [Adafruit Bicolor LED Square Pixel Matrix with I2C Backpack](https://www.adafruit.com/product/902)

1x Right-angled male headers for the LED matrix displays - ones where the right angle occurs above the plastic strip [like these](https://www.amazon.com/gp/product/B07ZHG25NH/), NOT below the strip [like these](https://www.adafruit.com/product/1540). (A subtle difference but one type will fit in the case while the other will not!) 

One or more of the sensors below. The IAQ will automatically detect which ones are present.

1x [Adafruit PMSA003I Air Quality Breakout](https://www.adafruit.com/product/4632)

1x [SCD-40 - True CO2, Temperature and Humidity Sensor](https://www.adafruit.com/product/5187)

1x [SGP30 Air Qulaity Sensor VOC and eC02](https://www.adafruit.com/product/3709)

1x [STEMMA QT / Qwiic JST SH 4-pin Cable - 200mm Long](https://www.adafruit.com/product/4401)

You'll need one of the following cables for each additional sensor beyond the first one:

1x - 2x [STEMMA QT / Qwiic JST SH 4-pin Cable - 50mm Long](https://www.adafruit.com/product/4399)

3x [STEMMA QT / Qwiic JST SH 4-pin Cable with Premium Female Sockets - 150mm Long](https://www.adafruit.com/product/4397)

1x [Raspberry Pi 3 Model A+](https://www.raspberrypi.org/products/raspberry-pi-3-model-a-plus/) (The software will run on a Pi 2, 3, or 4 but this is the specific Pi model to use for the custom case)

1x [SparkFun Qwiic Multiport](https://www.adafruit.com/product/4861) also available [here](https://www.sparkfun.com/products/18012)

## Assembly
The device itself requires no soldering, however the LED pixel matrix does need to be soldered to the I2C backpack as described [here](https://learn.adafruit.com/adafruit-led-backpack/bi-color-8x8-matrix-assembly). (You'll also need to change the I2C address of one of the LED matrix units to 0x71 by soldering together the A0 pads on the back.) If you are using our custom case, don't solder the included headers to the backpacks - use the angled ones described in the parts list above. All of the components that need to be wired together use I2C, so simply connect everything using the Qwiic multiport and the recommended cables. The two sensors can be daisy-chained, while the two LED backpacks only have headers, so they will need to use the cables with female header sockets on one end. Finally, connect the multiport to the Pi using a similar Qwiic to female header cable. See the diagram below:

![](https://raw.githubusercontent.com/balena-io-playground/balena-iaq/master/images/wiring.png)

## Software
You can use the button below to deploy this software to your device. If you don't already have a free [balenaCloud account](https://dashboard.balena-cloud.com/signup), you will be prompted to set one up first.

(button coming soon!)

Alternatively, you can clone this repo, create a new fleet, and push it to your device using the [balena CLI](https://www.balena.io/docs/reference/balena-cli/). This method is recommended if you want to potentially modify the project or do further development.

In either case, once you have clicked the deploy button (which will walk you through creating a fleet) or pushed the project using the CLI, next click the "Add device" button in your fleet. Choose the Raspberry Pi 3 (NOT 64 bit) and remember to enter your WiFi credentials since the Pi 3A+ does not have ethernet capability. Download the OS image file, burn it to a microSD card using [balena Etcher](https://www.balena.io/etcher/), insert the card into the Pi and then power it on.

The Pi will begin downloading the application and once it has completed and begins executing you should see activity on the LED display.

## Custom case
The custom case consists of four pieces that can be printed using a standard consumer 3D printer. The files for printing these pieces are in the `stl` folder. They are named as follows:

![](https://raw.githubusercontent.com/balena-io-playground/balena-iaq/master/images/case.png)

### Front
The front panel holds the LED/backpack assemblies. Each assembly slides onto a set of four posts and should be pushed down as far as possible until they rest on the larger diameter section of the posts. The backpack that is set to the 0x71 address by the solder pad blob should be on the right when looking at the back of the face plate. Use a hot soldering iron tip to melt the smaller part of the post to keep the displays in place. (Note newer versions of the front piece use screw holes instead of posts.) The angled headers should face upwards. TIP: attach the female wire headers before inserting the displays onto the posts.
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
