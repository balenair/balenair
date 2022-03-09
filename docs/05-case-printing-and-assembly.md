# Case printing and assembly

The IAQ has a lovely and easy-to-print 3D case that fits the standard parts listed in the hardware list.

## Hardware required

To assemble the printed parts, you'll need the following:

- eight (8) M1.4 x 5mm self-tapping screws to mount the display
- four (4) #2-56 5/8" pan head screws if you are using the LED bargraph display
- four (4) #2-56 pan head screws 1/4" to 5/16" long with optional nuts for mounting the Pi
- two (2) #2-56 1/2" long pan head screws for mounting the multiport connector
- six (6) #2-56 5/32" pan head screws to mount the sensors
- four (4) M3 x 40mm hex socket head screws to secure the case

## Printing

The IAQ case consists of four pieces that can be printed using a standard consumer 3D printer. The files for printing these pieces are in the `stl` folder.

![](https://raw.githubusercontent.com/balena-io-playground/balena-iaq/master/images/case.png)

We have tested these pieces by slicing them using Ultimaker Cura 4.11; Each piece should be rotated 180 degrees for printing. We used an infill density of 20%, which the printing characteristics below are based on.

### Front piece

The front panel holds the LED/backpack assemblies. Each assembly sits on a set of four posts. Use M1.4 x 5mm screws to secure the displays to the posts. The backpack that is set to the 0x71 address by the solder pad blob should be on the right when looking at the back of the face plate. The angled headers should face upwards. TIP: attach the female wire headers before inserting the displays onto the posts.
![](https://raw.githubusercontent.com/balena-io-playground/balena-iaq/master/images/case_front2.PNG)

If you are using the LED bargraph, also print the `bargraph-bracket.stl` piece. Attach the bargraph to the bracket as shown below, then attach the bracket to the front piece with the Qwiic connectors on the left side.

Printing tips: Note that the first layer is only one layer thick for the display window portion of the front piece. Since that adds a lot of surface area on the bed, you can probably get by with a skirt instead of a brim for this part. Typical printing characteristsics: 28g/9.4m of filament; 4:06 print time.

### Pi Ring
The `pi_ring` holds the Raspberry Pi 3A+ or Zero 2 W in place. Use four #2-56 pan head screws 1/4" to 5/16" long to mount the Pi in the provided holes. A longer screw will go through the pi_ring so a nut could be added to the other side for additional stability. Note the four cylidrical spacers that print along the right wall of the part. These are used to properly mount a Pi Zero 2 W - you can ignore or discard them if using a Pi 3A+. See the photos below for the proper mounting orientation of the two different Pi models:

![](https://raw.githubusercontent.com/balena-io-playground/balena-iaq/master/images/case_pi.png)

Printing tips: This piece does not have a lot of bed surface area, so a brim is recommended. Printing characteristics: 27g/9.04m of filament; 5:15 print time.

### Insulate sense
The `insulate_sense` piece is used to mount the sensors and insulate them from the heat of the Pi. There is a small opening at the bottom of this piece to feed a Qwiic connector and cable through to the other side to attach to the first sensor (usually the particulate unit). The side opposite the sensor mounts has two holes to attach the Qwiic multiport connector with #2-56 1/2" pan head screws and nuts.

There are mounting holes in the posts for all sensors. You can use two, three, or four #2-56 5/32" pan head screws to attach each sensor. For extra stability, use one or more 5/8" screw with a nut on the other end per sensor. The bottom of the particulate sensor "sits" on a small shelf. TIP: Tape the blue part of the particulate sensor to the circuit board with a small amount of electrical tape to keep it from sliding around. (Make sure not to cover any of the venting holes on the right of the sensor though!) You can daisy chain the sensors together using various length Qwiic connector cables.

![](https://raw.githubusercontent.com/balena-io-playground/balena-iaq/master/images/case_insulate.png)


![](https://raw.githubusercontent.com/balena-io-playground/balena-iaq/master/images/case_insulate_back.png)

Printing tips: This piece has a good amount of surface area on the bed, so a skirt may be sufficient. Printing characteristics: 31g/10.36m of filament; 3:42 print time.

### Back
The back of the unit provides protection and airflow for the sensors. All four pieces are held together by inserting four M3 x 40mm hex socket head screws through the back piece and attaching to the screw holes in the front piece. These screws should not thread into any piece other than the front - they should move freely until they hit the holes in the front. You may need to start the threading on the front piece by inserting a small wood screw and rotating it a few turns.

Printing tips: This piece has a limited amount of bed surface area, so a brim is recommended. In addition, you should enable the "generate support" option for placement "everywhere" and a support overhang angle of "45". Printing characteristics: 28g/8.04m of filament; 4:44 print time.
