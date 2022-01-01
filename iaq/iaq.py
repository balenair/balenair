# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# pylint: disable=unused-import
import time
import board
import busio
import json
from digitalio import DigitalInOut, Direction, Pull
from adafruit_pm25.i2c import PM25_I2C
from adafruit_max7219 import matrices
import paho.mqtt.client as mqtt
import os
import adafruit_sgp30
import binascii

import display

PM25_MAX = 250
PM10_MAX = 430
CO2_MAX = 5000
PM25_RED = 55
PM10_RED = 150
CO2_RED = 2000
PM25_YELLOW = 35
PM10_YELLOW = 54
CO2_YELLOW = 1000
CO2_MIN = 400
VOC_MIN = 0
VOC_MAX = 10000
VOC_YELLOW = 500
VOC_RED = 1000
pm_sensor = 1
scd_sensor = 1
voc_sensor = 1
bar_graph = 0
# Sleep time for each cycle. Normally 60 secs.
# Some other operations are derived from this:
cycle_time = 60
voc_baseline_count = 0
voc_baseline_eco2 = 0 # was 0x8973
voc_baseline_tvoc = 0 # was 0x8AAE
voc_baseline_limit = 60 * cycle_time


green_limit = 50
yellow_limit = 75

pm10_idx = 0
pm25_idx = 0
co2_idx = 0
voc_idx = 0

# Get ENV vars:

try:
    alert_mode = int(os.getenv('ALERT_MODE', '0'))
except Exception as e:
    print("Invalid value for ALERT_MODE. Using default 0.")
    alert_mode = 0

try:
    alert_level = int(os.getenv('ALERT_LEVEL', '50'))
except Exception as e:
    print("Invalid value for ALERT_LEVEL. Using default 50.")
    alert_level = 50
 
try:
    zero_bar = int(os.getenv('ZERO_BAR', '1'))
except Exception as e:
    print("Invalid value for ZERO_BAR. Using default 1.")
    zero_bar = 1

try:
    del_baseline = int(os.getenv('DELETE_BASELINE', '0'))
except Exception as e:
    print("Invalid value for DELETE_BASELINE. Using default 0.")
    del_baseline = 0
    
              
reset_pin = None
# If you have a GPIO, its not a bad idea to connect it to the RESET pin
# reset_pin = DigitalInOut(board.G0)
# reset_pin.direction = Direction.OUTPUT
# reset_pin.value = False


# For use with a computer running Windows:
# import serial
# uart = serial.Serial("COM30", baudrate=9600, timeout=1)

# For use with microcontroller board:
# (Connect the sensor TX pin to the board/computer RX pin)
# uart = busio.UART(board.TX, board.RX, baudrate=9600)

# For use with Raspberry Pi/Linux:
# import serial
# uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)

# For use with USB-to-serial cable:
# import serial
# uart = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=0.25)

# Connect to a PM2.5 sensor over UART
# from adafruit_pm25.uart import PM25_UART
# pm25 = PM25_UART(uart, reset_pin)

# Create library object, use 'slow' 100KHz frequency!
i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
# Connect to a PM2.5 sensor over I2C
try:
    pm25 = PM25_I2C(i2c, reset_pin)
except Exception as e:
    print("No PM2.5 sensor found...")
    pm_sensor = 0
else:
    print("Found PM2.5 sensor, reading data...")
    
# SPDX-FileCopyrightText: 2020 by Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import adafruit_scd4x

#i2c = board.I2C()
try:
    scd4x = adafruit_scd4x.SCD4X(i2c)
except Exception as e:
    print("No SCD sensor found...")
    scd_sensor = 0
else:
    print("Found SCD sensor: Serial number:", [hex(i) for i in scd4x.serial_number])

import board
from adafruit_ht16k33.matrix import Matrix8x8x2

#i2c = board.I2C()
try:
    matrix2 = Matrix8x8x2(i2c, address=0x70)
    matrix1 = Matrix8x8x2(i2c, address=0x71)
except Exception as e:
    print("No LED matrix found, using LED bar graph...")
    bar_graph = 1

#i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)

# Delete baseline file(s) if device variable set
if del_baseline != 0:
    print("Baseline file will be deleted!")
    print("Change DELETE_BASELINE device variable to 0 after delete!")
    if os.path.exists("/data/my_data/baseline-eco2.txt"):
        os.remove("/data/my_data/baseline-eco2.txt")
    else:
        print("The file /data/my_data/baseline-eco2.txt does not exist.")
    if os.path.exists("/data/my_data/baseline-tvoc.txt"):
        os.remove("/data/my_data/baseline-tvoc.txt")
    else:
        print("The file /data/my_data/baseline-tvoc.txt does not exist.") 
    
# Create library object on our I2C port
try:
    sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)
except Exception as e:
    print("No SGP VOC sensor found...")
    voc_sensor = 0
else:
    print("Found VOC sensor: SGP30 serial #", [hex(i) for i in sgp30.serial])
    try:
        f = open("/data/my_data/baseline-eco2.txt", "r")
    except Exception as e:
        print("No eCO2 baseline file found. Calculating new 12hr baseline...")
        voc_baseline_limit = 730 * cycle_time # 730 minutes = 12 hours
    else:
        voc_baseline_eco2 = int(f.read())
        f.close()
      
    try:
        f = open("/data/my_data/baseline-tvoc.txt", "r")
    except Exception as e:
        print("No TVOC baseline file found. Calculating new 12hr baseline...")
        voc_baseline_limit = 730 * cycle_time # 730 minutes = 12 hours
    else:
        voc_baseline_tvoc = int(f.read())
        f.close()
    sgp30.iaq_init()
    if (voc_baseline_eco2 != 0) and (voc_baseline_tvoc != 0):
        print("Setting VOC baseline from file.")
        sgp30.set_iaq_baseline(voc_baseline_eco2, voc_baseline_tvoc)
    print("Initial eCO2 = %d ppm \t TVOC = %d ppb" % (sgp30.eCO2, sgp30.TVOC))

# List for LED wiring configuration
# format: [LED0 grn, LED0 red, LED1 grn, LED1 red... LED7 grn, LED7 red]
# each entry is pixel [x, y] 
LED_config = [[0,6],[0,7],[0,4],[0,5],[0,2],[0,3],[0,0],[0,1],[1,6],[1,7],[1,4],[1,5],[1,2],[1,3],[1,0],[1,1]]

# For LED bar graph:
if bar_graph == 1:
    clk = board.SCK
    din = board.MOSI
    cs = DigitalInOut(board.CE0)

    spi = busio.SPI(clk, MOSI=din)
    bar_display = matrices.Matrix8x8(spi, cs)


def scd_sense():
    #
    # Take a reading from the CO2 sensor, return dict
    #
    scd_dict = {}
    count = 0
    while not scd4x.data_ready:
        count = count + 1
        print("Waiting for scd4x  measurement ({0})....".format(count))
        time.sleep(1)

    print("CO2: %d ppm" % scd4x.CO2)
    print("Temperature: %0.1f *C" % scd4x.temperature)
    print("Humidity: %0.1f %%" % scd4x.relative_humidity)
    print()

    scd_dict["co2"] = scd4x.CO2
    scd_dict["temperature"] = scd4x.temperature
    scd_dict["humidity"] = scd4x.relative_humidity
    
    return scd_dict

def pm_sense():
    #
    # Take a reading from the particulate sensor, return dict
    #
    try:
        aqdata = pm25.read()
    except RuntimeError:
        print("Unable to read from sensor, retrying...")
        time.sleep(1)
        try:
            aqdata = pm25.read()
        except RuntimeError:
            print("Unable to read from sensor, retrying (2)...")
            time.sleep(2)
            try:
                aqdata = pm25.read()
            except RuntimeError:
                print("Unable to read from sensor (3), skipping...")
                return {}

    print()
    print("Concentration Units (standard)")
    print("---------------------------------------")
    print(
        "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
        % (aqdata["pm10 standard"], aqdata["pm25 standard"], aqdata["pm100 standard"])
    )
    print("Concentration Units (environmental)")
    print("---------------------------------------")
    print(
        "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
        % (aqdata["pm10 env"], aqdata["pm25 env"], aqdata["pm100 env"])
    )
    print("---------------------------------------")
    print("Particles > 0.3um / 0.1L air:", aqdata["particles 03um"])
    print("Particles > 0.5um / 0.1L air:", aqdata["particles 05um"])
    print("Particles > 1.0um / 0.1L air:", aqdata["particles 10um"])
    print("Particles > 2.5um / 0.1L air:", aqdata["particles 25um"])
    print("Particles > 5.0um / 0.1L air:", aqdata["particles 50um"])
    print("Particles > 10 um / 0.1L air:", aqdata["particles 100um"])
    print("---------------------------------------")

    return aqdata

def voc_sense():
    #
    # Take a reading from the VOC SGP30 sensor, return dict
    #
    voc_dict = {}
    print("eCO2 = %d ppm \t TVOC = %d ppb" % (sgp30.eCO2, sgp30.TVOC))
    voc_dict["eCO2"] = sgp30.eCO2
    voc_dict["TVOC"] = sgp30.TVOC

    return voc_dict

def pm25_index(pm25):
    #
    # Calculates our 0-99 AQ index for pm25
    #
    scaled_pm25 = 0

    if pm25 < PM25_YELLOW:
        scaler = make_interpolater(0, PM25_YELLOW, 0, 50)
        scaled_pm25 = scaler(pm25)
    elif pm25 < PM25_RED:
        scaler = make_interpolater(PM25_YELLOW, PM25_RED, 50, 75)
        scaled_pm25 = scaler(pm25)
    else:
        scaler = make_interpolater(PM25_RED, PM25_MAX, 75, 99)
        scaled_pm25 = scaler(pm25)
    
    
    if scaled_pm25 > 99:
        scaled_pm25 = 99
        
    return scaled_pm25

def pm10_index(pm10):
    #
    # Calculates our 0-99 AQ index for pm10
    #
    scaled_pm10 = 0

    if pm10 < PM10_YELLOW:
        scaler = make_interpolater(0, PM10_YELLOW, 0, 50)
        scaled_pm10 = scaler(pm10)
    elif pm10 < PM10_RED:
        scaler = make_interpolater(PM10_YELLOW, PM10_RED, 50, 75)
        scaled_pm10 = scaler(pm10)
    else:
        scaler = make_interpolater(PM10_RED, PM10_MAX, 75, 99)
        scaled_pm10 = scaler(pm10)

    if scaled_pm10 > 99:
        scaled_pm10 = 99
        
    return scaled_pm10

def co2_index(co2):
    #
    # Calculates our 0-99 AQ index for co2
    #
    scaled_co2 = 0

    if co2 < CO2_YELLOW:
        scaler = make_interpolater(CO2_MIN, CO2_YELLOW, 0, 50)
        scaled_co2 = scaler(co2)
    elif co2 < CO2_RED:
        scaler = make_interpolater(CO2_YELLOW, CO2_RED, 50, 75)
        scaled_co2 = scaler(co2)
    else:
        scaler = make_interpolater(CO2_RED, CO2_MAX, 75, 99)
        scaled_co2 = scaler(co2)
    
    if scaled_co2 > 99:
        scaled_co2 = 99
        
    return scaled_co2

def voc_index(voc):
    #
    # Calculates our 0-99 AQ index for VOC
    #
    scaled_voc = 0

    if voc < VOC_YELLOW:
        scaler = make_interpolater(VOC_MIN, VOC_YELLOW, 0, 50)
        scaled_voc = scaler(voc)
    elif voc < VOC_RED:
        scaler = make_interpolater(VOC_YELLOW, VOC_RED, 50, 75)
        scaled_voc = scaler(voc)
    else:
        scaler = make_interpolater(VOC_RED, VOC_MAX, 75, 99)
        scaled_voc = scaler(voc)
    
    if scaled_voc > 99:
        scaled_voc = 99

    return scaled_voc
       
def make_interpolater(left_min, left_max, right_min, right_max):
    #
    # Scales one range to another...
    # Function that returns a function (closure)
    # see https://stackoverflow.com/questions/1969240/mapping-a-range-of-values-to-another
    #

    # Figure out how 'wide' each range is  
    leftSpan = left_max - left_min  
    rightSpan = right_max - right_min  

    # Compute the scale factor between left and right values 
    scaleFactor = float(rightSpan) / float(leftSpan) 

    # create interpolation function using pre-calculated scaleFactor
    def interp_fn(value):
        return right_min + (value-left_min)*scaleFactor

    return interp_fn
    

def rotate_matrix( m ):
    #
    # Rotate digit matrix by 90 degrees counterclockwise
    # see https://stackoverflow.com/questions/53250821/in-python-how-do-i-rotate-a-matrix-90-degrees-counterclockwise
    #
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0])-1,-1,-1)]

def display_index(index_value):
    #
    # Display a two digit number on the LEDs
    #
    if bar_graph == 1:
        print("Skipping LED matrix display...")
        bar_index(index_value)
        return
    my_color = 0
    if round(index_value) < green_limit:
        my_color = 2
    elif round(index_value) < yellow_limit:
        my_color = 3
    else:
        my_color = 1
            
    disp_val = str(round(index_value)).rjust(2)

    left_digit = disp_val[:1]
    right_digit = disp_val[-1:]

    display_led(matrix1, left_digit, my_color)
    display_led(matrix2, right_digit, my_color)
    
def display_led(my_matrix, my_value, color):
    #
    # Display a single digit
    #
    if my_value == ' ':
        my_digit = display.digits[0]
    else:
        my_digit = display.digits[int(my_value)]

    my_digit = rotate_matrix(my_digit)
    for x in range(8):
        for y in range(8):
            if my_digit[x][y] == 1:
                my_matrix[x,y] = color
            else:
                my_matrix[x,y] = my_matrix.LED_OFF

def display_pollutant(pm10, pm25, co2, voc):
    #
    # Display a two character icon on the LEDs
    #  representing highest-indexed pollutant
    #  Uses icons list 0/1=PM1, 2/3=PM2, 4/5=CO2
    #
    index_list = [pm10, pm25, co2, voc]
    max_value = max(index_list)
    max_value_index = index_list.index(max_value)
    icon_index = max_value_index * 2
        
    my_color = 0
    if round(max_value) < green_limit:
        my_color = 2
    elif round(max_value) < yellow_limit:
        my_color = 3
    else:
        my_color = 1
    #print("display...")
    #print("max value {0}".format(max_value))
    #print("my_color {0}".format(my_color))
    display_icon(icon_index, my_color)
    
    
def display_icon(icon_index, my_color):
    #
    # Display a two character icon on the display
    # icon_index is the index of the first character
    #
    if bar_graph == 1:
        print("Skipping LED matrix icon display...")
        return
    for digit in range(2):
      if digit == 0:
          my_matrix = matrix1
      else:
          my_matrix = matrix2
      my_digit = display.icons[icon_index + digit]
      my_digit = rotate_matrix(my_digit)
      for x in range(8):
          for y in range(8):
              if my_digit[x][y] == 1:
                  my_matrix[x,y] = my_color
              else:
                  my_matrix[x,y] = my_matrix.LED_OFF

def LED_control(LED, color):
    # 
    # Turns an LED on in buffer and sets its color - still must call display()
    # LED can be 0 - 7 (L to R)
    # color can be "red", "green", or "yellow"
    #
    #print("LED CONTROL {0},{1}".format(LED, color))
    if (LED < 0) or (LED > 7):
        return

    green_led = LED_config[LED * 2]
    red_led = LED_config[(LED * 2) + 1]

    if (color == "red") or (color == "yellow"):
        bar_display.pixel(red_led[0], red_led[1], 1)
    if (color == "green") or (color == "yellow"):
        bar_display.pixel(green_led[0], green_led[1], 1)

def bar_index(idx):
    #
    # Display an index on the LEDs
    # idx = 0 - 99
    # bar color chosen by green_limit, yellow_limit
    #
    if idx > 99:
        idx = 99

    print("Calling bar_index {}".format(idx))
    bar_display.clear_all()
    for i in range(8):
        if (idx > (i) * 12.4):
            if idx < green_limit:
                LED_control(i, "green")
            elif idx > yellow_limit:
                LED_control(i, "red")
            else:
                LED_control(i, "yellow")

    # Show first LED for zero index (can be disabled by user)
    if (idx == 0) and (zero_bar == 1):
        LED_control(0, "green")

    bar_display.show()
    bar_display.brightness(10)

# START

# Make sure there's at least one sensor

if max(pm_sensor, scd_sensor, voc_sensor) < 1:
    display_icon(8, 1)
    print("No sensors found! Exiting...")
    sys.exit()
 
if pm_sensor == 1:
    display_icon(0, 2)
    time.sleep(2)
    display_icon(2, 2)
    time.sleep(1)
if voc_sensor == 1:
    display_icon(6, 2)
    time.sleep(2)
    
if scd_sensor == 1:
    display_icon(4, 2)
    time.sleep(1)
    scd4x.start_periodic_measurement()
    print("Waiting for scd4x  measurement....")

# Bar graph startup animation
if bar_graph == 1:
    for i in range(1,100, 5):
        bar_index(i)
        time.sleep(0.15)
    bar_index(0)

client = mqtt.Client()
try:
    client.connect("mqtt", 1883, 60)
except Exception as e:
    print("Error connecting to mqtt. ({0})".format(str(e)))
else:
    client.loop_start()

while True:
    pm = {}
    scd = {}
    voc = {}
    if pm_sensor == 1:
        print("Testimg PM...")
        pm = pm_sense()
        pm10_idx = pm10_index(pm["pm100 standard"])
        pm25_idx = pm25_index(pm["pm25 standard"])
    if scd_sensor == 1:
        print("Testing SCD...")
        scd = scd_sense()
        co2_idx = co2_index(scd["co2"])
    if voc_sensor == 1:
        print("Testing VOC...")
        voc = voc_sense()
        voc_idx = voc_index(voc["TVOC"])
        if scd_sensor == 0:
            # Use eCO2 for CO2
            co2_idx = co2_index(voc["eCO2"])
    # Merge dictionaries into scd:
    # If sensor does not exist, neither will its fields
    scd.update(pm)
    scd.update(voc)
    print("Scaled pm25: {0}".format(pm25_idx))
    print("Scaled pm10: {0}".format(pm10_idx))
    print("Scaled co2: {0}".format(co2_idx))
    print("Scaled voc: {0}".format(voc_idx))  
    iaq_idx = max(pm25_idx, pm10_idx, co2_idx, voc_idx)
    # Add index to dict
    scd["IAQ"] = iaq_idx
    print("Using index: {0}".format(iaq_idx))
    # Display on LED matrix
    display_index(iaq_idx)
    # Publish all data to MQTT
    try:
        client.publish("sensors", json.dumps(scd))
    except Exception as e:
        print("Error publishing to mqtt. ({0})".format(str(e)))
        
    # Alternate display with icon every 2.5 seconds if index > green_limit
    if ((iaq_idx > alert_level) and (alert_mode == 1)) or (alert_mode == 2):
        time.sleep(2.5)
        for recur in range(11):
            display_pollutant(pm10_idx, pm25_idx, co2_idx, voc_idx)
            time.sleep(2.5)
            display_index(iaq_idx)
            time.sleep(2.5)
    
    else:
        time.sleep(cycle_time)

    if voc_sensor == 1:    
        voc_baseline_count = voc_baseline_count + 1
        print("VOC baseline count: {0}, saving in {1} iteration(s).".format(voc_baseline_count, voc_baseline_limit - voc_baseline_count))
        if voc_baseline_count == voc_baseline_limit:
            print("Saving VOC baseline values... CO2eq = {0}, TVOC = {1}".format(sgp30.baseline_eCO2, sgp30.baseline_TVOC))
            # Add a save routine here
            try:
                f = open("/data/my_data/baseline-eco2.txt", "w")
            except Exception as e:
                print("Error saving eCO2 baseline...")
            else:
                f.write(str(sgp30.baseline_eCO2))
                f.close()

            try:
                f = open("/data/my_data/baseline-tvoc.txt", "w")
            except Exception as e:
                print("Error saving TVOC baseline...")
            else:
                f.write(str(sgp30.baseline_TVOC))
                f.close()

            voc_baseline_count = 0
