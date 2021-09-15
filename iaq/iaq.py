# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Example sketch to connect to PM2.5 sensor with either I2C or UART.
"""

# pylint: disable=unused-import
import time
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
from adafruit_pm25.i2c import PM25_I2C

PM25_MAX = 250
PM10_MAX = 430
CO2_MAX = 5000
PM25_RED = 55
PM10_RED = 150
CO2_RED = 2000
PM25_YELLOW = 35
PM10_YELLOW = 54
CO2_YELLOW = 1000

digits = [[[1,1,1,1,1,1,1,0],
       [1,1,1,1,1,1,1,0],
       [1,1,0,0,0,1,1,0],
       [1,1,0,0,0,1,1,0],
       [1,1,0,0,0,1,1,0],
       [1,1,0,0,0,1,1,0],
       [1,1,1,1,1,1,1,0],
       [1,1,1,1,1,1,1,0]],      
       [[0,1,1,1,0,0,0,0],
       [0,1,1,1,0,0,0,0],
       [0,0,1,1,0,0,0,0],
       [0,0,1,1,0,0,0,0],
       [0,0,1,1,0,0,0,0],
       [0,0,1,1,0,0,0,0],
       [1,1,1,1,1,1,0,0],
       [1,1,1,1,1,1,0,0]],
       [[1,1,1,1,1,1,1,0],
       [1,1,1,1,1,1,1,0],
       [0,0,0,0,0,1,1,0],
       [1,1,1,1,1,1,1,0],
       [1,1,1,1,1,1,1,0],
       [1,1,0,0,0,0,0,0],
       [1,1,1,1,1,1,1,0],
       [1,1,1,1,1,1,1,0]],
       [[1,1,1,1,1,1,1,0],
       [1,1,1,1,1,1,1,0],
       [0,0,0,0,0,1,1,0],
       [1,1,1,1,1,1,1,0],
       [1,1,1,1,1,1,1,0],
       [0,0,0,0,0,1,1,0],
       [1,1,1,1,1,1,1,0],
       [1,1,1,1,1,1,1,0]],
       [[1,1,0,0,0,0,0,0],
       [1,1,0,1,1,0,0,0],
       [1,1,0,1,1,0,0,0],
       [1,1,1,1,1,1,1,0],
       [1,1,1,1,1,1,1,0],
       [0,0,0,1,1,0,0,0],
       [0,0,0,1,1,0,0,0],
       [0,0,0,1,1,0,0,0]],
       [[1,1,1,1,1,1,1,0],
       [1,1,1,1,1,1,1,0],
       [1,1,0,0,0,0,0,0],
       [1,1,1,1,1,1,1,0],
       [1,1,1,1,1,1,1,0],
       [0,0,0,0,0,1,1,0],
       [1,1,1,1,1,1,1,0],
       [1,1,1,1,1,1,1,0]],
       [[1,1,1,1,1,1,1,0],
       [1,1,1,1,1,1,1,0],
       [1,1,0,0,0,0,0,0],
       [1,1,1,1,1,1,1,0],
       [1,1,1,1,1,1,1,0],
       [1,1,0,0,0,1,1,0],
       [1,1,1,1,1,1,1,0],
       [1,1,1,1,1,1,1,0]],
       [[1,1,1,1,1,1,1,0],
       [1,1,1,1,1,1,1,0],
       [0,0,0,0,0,1,1,0],
       [0,0,0,0,1,1,0,0],
       [0,0,0,1,1,0,0,0],
       [0,0,1,1,0,0,0,0],
       [0,1,1,0,0,0,0,0],
       [1,1,0,0,0,0,0,0]],   
       [[1,1,1,1,1,1,1,0],
       [1,1,1,1,1,1,1,0],
       [1,1,0,0,0,1,1,0],
       [1,1,1,1,1,1,1,0],
       [1,1,1,1,1,1,1,0],
       [1,1,0,0,0,1,1,0],
       [1,1,1,1,1,1,1,0],
       [1,1,1,1,1,1,1,0]],
       [[1,1,1,1,1,1,1,0],
       [1,1,1,1,1,1,1,0],
       [1,1,0,0,0,1,1,0],
       [1,1,1,1,1,1,1,0],
       [1,1,1,1,1,1,1,0],
       [0,0,0,0,0,1,1,0],
       [1,1,1,1,1,1,1,0],
       [1,1,1,1,1,1,1,0]]]
           
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
pm25 = PM25_I2C(i2c, reset_pin)

print("Found PM2.5 sensor, reading data...")

# SPDX-FileCopyrightText: 2020 by Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import adafruit_scd4x

i2c = board.I2C()
scd4x = adafruit_scd4x.SCD4X(i2c)
print("Found SCD sensor: Serial number:", [hex(i) for i in scd4x.serial_number])

import board
from adafruit_ht16k33.matrix import Matrix8x8x2

i2c = board.I2C()
matrix2 = Matrix8x8x2(i2c, address=0x70)
matrix1 = Matrix8x8x2(i2c, address=0x71)


def scd_sense():
    #
    # Take a reading from the CO2 sensor, return dict
    #
    scd_dict = {}
    #scd4x.start_periodic_measurement()
    #print("Waiting for scd4x  measurement....")
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
        # print(aqdata)
    except RuntimeError:
        print("Unable to read from sensor, retrying...")
        

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

def my_index(pm25, pm10, co2):
    #
    # Calculates our 0-99 AQ index based on three inputs
    #
    idx = 0
    scaled_pm25 = 0
    scaled_pm100 = 0
    scaled_co2 = 0

    if pm25 < PM25_YELLOW:
        scaler = make_interpolater(0, PM25_YELLOW, 0, 50)
        scaled_pm25 = scaler(pm25)
    elif pm25 < PM25_RED:
        scaler = make_interpolater(PM25_YELLOW, PM25_RED, 50, 75)
        scaled_pm25 = scaler(pm25)
    else:
        scaler = make_interpolater(PM25_RED, PM25_MAX, 75, 99)
        scaled_pm25 = scaler(pm25)

    if pm10 < PM10_YELLOW:
        scaler = make_interpolater(0, PM10_YELLOW, 0, 50)
        scaled_pm10 = scaler(pm10)
    elif pm10 < PM10_RED:
        scaler = make_interpolater(PM10_YELLOW, PM10_RED, 50, 75)
        scaled_pm10 = scaler(pm10)
    else:
        scaler = make_interpolater(PM10_RED, PM10_MAX, 75, 99)
        scaled_pm10 = scaler(pm10)

    if co2 < CO2_YELLOW:
        scaler = make_interpolater(0, CO2_YELLOW, 0, 50)
        scaled_co2 = scaler(co2)
    elif co2 < CO2_RED:
        scaler = make_interpolater(CO2_YELLOW, CO2_RED, 50, 75)
        scaled_co2 = scaler(co2)
    else:
        scaler = make_interpolater(CO2_RED, CO2_MAX, 75, 99)
        scaled_co2 = scaler(co2)

    print("Scaled pm25: {0}".format(scaled_pm25))
    print("Scaled pm10: {0}".format(scaled_pm10))
    print("Scaled co2: {0}".format(scaled_co2))

    return int(max(scaled_pm25, scaled_pm10, scaled_co2))

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
    #
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0])-1,-1,-1)]

def display_index(index_value):
    #
    # Display a two digit number on the LEDs
    #
    green_limit = 50
    yellow_limit = 75
    my_color = 0
    if index_value < green_limit:
        my_color = 2
    elif index_value < yellow_limit:
        my_color = 3
    else:
        my_color = 1

            
    disp_val = round(index_value)

    left_digit = str(disp_val)[:1]
    right_digit = str(disp_val)[-1:]

    display_led(matrix1, left_digit, my_color)
    display_led(matrix2, right_digit, my_color)
    
def display_led(my_matrix, my_value, color):
    #
    # Display a single digit
    #
    my_digit = digits[int(my_value)]
    my_digit = rotate_matrix(my_digit)
    for x in range(8):
        for y in range(8):
            if my_digit[x][y] == 1:
                my_matrix[x,y] = color
            else:
                my_matrix[x,y] = my_matrix.LED_OFF


# START

scd4x.start_periodic_measurement()
print("Waiting for scd4x  measurement....")

while True:
    pm = {}
    scd = {}
    print("Testimg PM...")
    pm = pm_sense()
    print("Testing SCD...")
    scd = scd_sense()
    # Merge two dictionaries into scd:
    scd.update(pm)
    # Get the custom index:
    idx = my_index(scd["pm25 standard"], scd["pm100 standard"], scd["co2"])
    print("Using index: {0}".format(idx))
    # Display on LED matrix
    display_index(idx)
    #TODO: code here to publish scd for charts and graphs
    time.sleep(55)
