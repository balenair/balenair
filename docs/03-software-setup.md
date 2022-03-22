# 3. Software setup

Now that you have your hardware set up and connected, it's time to install the software...

At a minimum, you'll need software to flash the SD card that will be inserted into the Raspberry Pi. We recommend [balenaEtcher](https://balena.io/etcher).

There are three main ways to deploy the software to your device...

## The open fleet option
If you want the simplest software deployment and automatic updates for your device, choose this option. An open fleet is a group of devices that all run the same code that anyone can join. We make it easy to join open fleets on balenaHub, our platform for IoT users to exchange resources. To join your device to the IAQ open fleet, click here.

Next click on the "get started" button and choose your model of Raspberry Pi from the dropdown list. For "Network Connection" choose "WiFi + Ethernet" and enter your WiFi SSID and password. (Note: these credentials are only stored inside the file you will be downloading and are not saved anywhere else.) Now, click the "Flash" button which will open balenaEtcher (if previously installed) and guide you through flashing the image to your microSD card.

### Notes about open fleets
- You don't need a balenaCloud account (free or paid) to join an open fleet

- The "fleet owner" for this open fleet is balena itself

- Your device's sensor data is potentially visible to the fleet owner, but not other members of the fleet

- balena does not save or view your sensor data except as needed for troubleshooting purposes

- If you want a private fleet (where you will be the fleet owner) choose one of the other two options below

## One-click deploy option
This option allows you to deploy and configure the IAQ with the single click of a button. It will create a new private fleet in your balenaCloud account. If you don't already have a free balenaCloud account, it will prompt you to create one. Use the button below to get started:

[deploy button]

![sdcard](https://raw.githubusercontent.com/balenalabs/balena-sound/master/docs/images/sdcard.gif)

Once your application has been created you'll need to add a device to it:

1. Add a device to the application by clicking the `add device` button. Don't forget to add WiFi credentials here if applicable!
2. Download the OS and flash it to your SD card with [balenaEtcher](https://balena.io/etcher)
3. Power up your device and check it's online in the dashboard!

The IAQ application will start downloading as soon as your device appears in the dashboard.

## Balena CLI option

This is the traditional and more advanced approach for deploying applications to balena powered devices. Choose this option if you want to customize or modify the code before deploying to your device. You could also use this option if you want to add or alter the services in the project by editing the `docker-compose.yml` file.

### Provision your device

1. Sign up for or login to the [balenaCloud dashboard](https://dashboard.balena-cloud.com)
2. Create an application, selecting the correct device type. (See the list of supported devices)
3. Add a device to the application, enabling you to download the OS
4. Flash the downloaded OS to your SD card with [balenaEtcher](https://balena.io/etcher)
5. Power up your device and check it's online in the dashboard

### Deploy the application

- Install the [balena CLI tools](https://github.com/balena-io/balena-cli/blob/master/INSTALL.md)
- Login with `balena login`
- Download [this project] and from the project directory run `balena push <appName>` where `<appName>` is the name you gave your balenaCloud application in the first step.

## Having trouble?

If you are running into issues getting your IAQ software running, please try the following:
1. Check the [support and troubleshooting guide](../support) for common issues and how to resolve them.
2. Post in the [forums] for help from our growing community.
3. Create an issue on the [IAQ GitHub project] if you find your issue may be a bug or problem with the IAQ software.

### NEXT
[4. Use and configuration](https://github.com/balena-io-playground/balena-iaq/blob/new-docs/docs/04-use-and-configuration.md)
