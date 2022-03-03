# Hardware selection

There are a number of options when it comes to selecting hardware for the IAQ. Cost, availability and performance are some factors to consider when choosing the parts below.

## Choosing your Pi

The IAQ runs on a Raspberry Pi, so you'll need one of the following compatible devices:

- A [Pi 3A+](https://www.raspberrypi.com/products/raspberry-pi-3-model-a-plus/) or [Pi Zero 2 W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/) will fit in the custom case, so one of these is the best choice
- A [Pi 3B](https://www.raspberrypi.com/products/raspberry-pi-3-model-b/), [Pi 3B+](https://www.raspberrypi.com/products/raspberry-pi-3-model-b-plus/), [Pi 4](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/), [CM4](https://www.raspberrypi.com/products/compute-module-4/?variant=raspberry-pi-cm4001000) or [CM3+](https://www.raspberrypi.com/products/compute-module-3-plus/) based system (Like the [balenaFin](https://www.balena.io/fin/)) will work fine but will not fit in the custom case.

(The IAQ is not compatible with the Pi Zero or first generation Pi)  

The IAQ is not particularly resource-intensive, so any of the supported boards above should work equally well. Note that currently the Pi Zero 2 W is only available without headers soldered in place. If you choose this device, you'll need to solder headers or wires onto the board. You could also try a "[solderless hammer header](https://shop.pimoroni.com/products/gpio-hammer-header?variant=35643318026)" although we have not tested these.

## Choosing your sensors

The sensors evaluate your air and return data that is used to deterime your air quality score. The IAQ supports the three different sensors listed below. You can choose to have one, two, or all three present in your device, depending on your budget and air quality analysis needs.

| Sensor | Detects | Description | cost (USD) | specifications (approx.) |
| ------------ | ----------- | ----------- | ----------- | ----------- |
| Particle | Smoke, dust, dirt, pollen | [PMSA003I](https://www.adafruit.com/product/4632) laser-scattering type | $44.95 | 0.3-1.0,1.0-2.5, 2.5-10 Micrometer particles |
| CO2 (plus temp and humidity) | Exhaled breath and burning fossil fuels | [SCD-40](https://www.adafruit.com/product/5187) photoacoustic sensor | $49.50 | 400 - 2000 PPM |
| VOC | Gasses emitted by solid and liquid products  | [SGP-30](https://www.adafruit.com/product/3709) Hot-plate MOX sensor | $17.50 | eCO2 400-60,000 ppm, TVOC 0-60,000 ppb |

All of these sensors use the popular I2C protocol to communicate with the Pi and include [Qwiic](https://www.sparkfun.com/qwiic) connectors so you don't need to do any soldering to use these sensors.

The IAQ will automatically detect which sensors are present and caluclate the air quality score accordingly.

## Choosing your display

Each IAQ device has a bright LED display so you can read your score from across a room. The score will be calculated and displayed even if your device is not connected to the internet. Regardless of the display type you choose, you can still obtain detailed sensor and air quality score readings from the built-in web dashboard.

### Two digit bi-color LED matrix

This is the most detailed display and also the most expensive. It utilizes two $15.95 [LED Square Pixel Matrix with I2C Backpack](https://www.adafruit.com/product/902) boards which also require some light soldering to install the connecting headers. You'll need to use angled headers, not the straight ones included with the boards. These should be right-angled male headers where the right angle occurs above the plastic strip [like these](https://www.amazon.com/Uxcell-a15062500ux0349-Single-40-pin-Breadboard/dp/B01461DQ6S/), NOT below the strip [like these](https://www.adafruit.com/product/1540). (A subtle difference but one type will fit in the case while the other will not!) If you are not using our custom case, you can just use the headers that are included with the display boards. These displays can be mounted directly on posts in the custom case with no modifications required.

The matrix displays are driven via I2C and require two [Qwiic to female header](https://www.adafruit.com/product/4397) cables to connect to the Pi. 

In addition to displaying the two digit score, these displays can optionally show the most dominant pollutant type (CO2, PM10, PM2.5, VOC) detected by the sensors, as well as some rudimentary animations. The displayed information will change color from green to orange to red depending on the score.

To summarize the parts for this option:

- Two [LED Square Pixel Matrix with I2C Backpack](https://www.adafruit.com/product/902)

- One strip of [angled male headers](https://www.amazon.com/Uxcell-a15062500ux0349-Single-40-pin-Breadboard/dp/B01461DQ6S/)

- Two [Qwiic to female header](https://www.adafruit.com/product/4397) cables

### 12 LED bi-color bargraph

This type of display is less detailed than the two digit matrix (the score is broken into 12 segments with each one representing 8.33 points) and can't display the pollutant type. It does however have the green/orange/red color indications and can be configured in three different display formats.

This option is about $13 or less than half the cost of the LED matrix. Currently this option is a somewhat complex build and requires soldering components onto a protoboard. The components include the [LED bargraph](https://www.adafruit.com/product/1719), a [MAX 7219](https://www.adafruit.com/product/453) display driver, and a [74AHCT125](https://www.adafruit.com/product/1787) quad level shifter IC. In the near future we hope to offer a pre-etched version of the PCB, but for now if you are interested in this display, see these instructions.

### Single bi-color LED

This is the simplest and least expensive display at about $7 in parts. It is also the only display option that requires no soldering. (If you choose this option, you can build the entire IAQ without any soldering.) Since it is just a single LED, it can only tell you if the air quality is good, moderate, or poor based on the color. You'll need the following parts for this option:

- One [18mm Red/Green LED](https://www.adafruit.com/product/4042)

- One [tiny breadboard](https://www.adafruit.com/product/65)

- One [220 ohm resistor](https://www.adafruit.com/product/2780) pack. (You'll have 23 left over in this pack. If you have any resistors lying around, any between 120 - 560 ohm should work fine.)

- One set of [female/male jumper cables](https://www.adafruit.com/product/5018) (We'll need 3 of the 10 jumpers included.)

## Remaining parts list

Regardless of the options above, you'll need the following parts:

- One SparkFun Qwiic multiport, available [here](https://www.adafruit.com/product/4861) and [here](https://www.sparkfun.com/products/18012)

- One [Qwiic to female header cable](https://www.adafruit.com/product/4397) to connect the multiport to the Pi

- One [200mm QT to QT cable](https://www.adafruit.com/product/4401) to connect the multiport to the first sensor.

- One [100mm QT to QT cable](https://www.adafruit.com/product/4210) to connect the first sensor to the second sensor. Only required if you have two or three sensors!

- Another [100mm QT to QT cable](https://www.adafruit.com/product/4210) to connect the second sensor to the third sensor. Only required if you have three sensors!
