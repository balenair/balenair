# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries SPDX-License-Identifier: MIT
# pylint: disable=unused-import
import time
import board
import busio
import json
import qwiic_led_stick
import paho.mqtt.client as mqtt
import os
import sys
import binascii
import display
import logging
from adafruit_ht16k33.matrix import Matrix8x8x2
import requests

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

pm_sensor = True
co2_sensor = True
voc_sensor = True
use_eco2 = False
sensor_count = 0
use_tvoc = True

bar_graph = False
matrix_display = False

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
    bar_mode = int(os.getenv('BAR_MODE', '1'))
except Exception as e:
    print("Invalid value for BAR_MODE. Using default 1.")
    bar_mode = 1

try:
    t = int(os.getenv('USE_TVOC', '1'))
except Exception as e:
    print("Invalid value for USE_TVOC. Using default 1.")
    use_tvoc = True
if t == 0:
    use_tvoc = False
    
try:
    log_level = os.getenv('LOG_LEVEL', 'WARNING')
except Exception as e:
    print("Invalid value for LOG_LEVEL. Using default 'WARNING'.")
    log_level = 'WARNING'
   
# Variables for optional Aggregator:
 
agg_address = os.getenv('AGG_ADDRESS', 'NONE')

try:
    agg_port = int(os.getenv('AGG_PORT', '1883'))
except Exception as e:
    print("Invalid value for AGG_PORT. Using default 1883.")
    agg_port = 1883

agg_username = os.getenv('AGG_USERNAME')

agg_password = os.getenv('AGG_PASSWORD')

agg_data = {}

#
# Get a meaningful host hame from balenaCloud device name and add it to mqtt topic, this allows easier
# grafana graphing in a multi device setup while using mqtt bridging. 
# 
try:
    r = requests.get(os.getenv('BALENA_SUPERVISOR_ADDRESS') + "/v2/device/name?apikey=" + os.getenv('BALENA_SUPERVISOR_API_KEY'))
    j = r.json()
    pretty_host_name = j["deviceName"]
except Exception as e:
    print("Unable to get deviceName via Supervisor API. Using default value.")
    pretty_host_name = "location"
pretty_host_name = pretty_host_name.replace("/", "_")
pretty_host_name = pretty_host_name.replace("'", "_")
pretty_host_name = pretty_host_name.replace("$", "_")
pretty_host_name = pretty_host_name.replace("+", "_")
pretty_host_name = pretty_host_name.replace("#", "_")
pretty_host_name = pretty_host_name.replace(" ", "_")

# Set up logger
logger = logging.getLogger('iaq_logger')
logger.setLevel(logging.DEBUG)  # Passes all messages to handlers

# Create handlers
c_handler = logging.StreamHandler(stream=sys.stdout)

if log_level == 'DEBUG':
    c_handler.setLevel(logging.DEBUG)
elif log_level == 'INFO':
    c_handler.setLevel(logging.INFO)
elif log_level == 'WARNING':
    c_handler.setLevel(logging.WARNING)
elif log_level == 'ERROR':
    c_handler.setLevel(logging.ERROR)
elif log_level == 'CRITICAL':
    c_handler.setLevel(logging.CRITICAL)
else:
    c_handler.setLevel(logging.WARNING)

print("log_level: {}".format(log_level))    
# Add handlers to the logger
logger.addHandler(c_handler)

logger.critical("You will see CRITICAL log entries.")
logger.debug("You will see DEBUG log entries.")
logger.error("You will see ERROR log entries.")
logger.warning('You will see WARNING log entries.')
logger.info("You will see INFO log entries.")

# Create library object, use 'slow' 10KHz frequency!
i2c = busio.I2C(board.SCL, board.SDA, frequency=10000)

try:
    matrix2 = Matrix8x8x2(i2c, address=0x70)
    matrix1 = Matrix8x8x2(i2c, address=0x71)
except Exception as e:
    logger.info("Only one or no LED matrix found, not using LED matrix...")
else:
    matrix_display = True

# For LED bar graph:
my_stick = qwiic_led_stick.QwiicLEDStick()
if my_stick.begin() == True:
    bar_graph = True
    time.sleep(1.5)
    try:
        my_stick.LED_off()
    except Exception as e:
        logger.info("Error accessing LED stick: {}".format(e))
else:
    logger.info("No LED stick found, not using LED stick...")

def get_reading():

    global sensor_count
    
    readings = {}

    try:
        r = requests.get('http://sensor:7575/')
    except Exception as e:
        logger.error("Error requesting sensor reading: {}".format(e))
        return readings
        
    j = r.json()

    #print("raw: {}".format(j))

    for sensor, measurement in j.items():
        #print("item: {}".format(sensor))
        if sensor == "PM25":
            readings.update(measurement)
        else:
            for key, item in measurement.items():
                #print("key: {}".format(key))
                if key == "temperature":
                    if not "temperature" in readings:
                        readings["temperature"] = item
                if key == "humidity":
                    if not "humidity" in readings:
                        readings["humidity"] = item
                if key == "CO2":
                    if not "co2" in readings:
                        sensor_count = sensor_count + 1
                        readings["co2"] = item
                if (key == "TVOC") and (use_tvoc):
                    if not "TVOC" in readings:
                        sensor_count = sensor_count + 1
                        readings["TVOC"] = item
                if key == "eCO2":
                    if not "eCO2" in readings:
                        sensor_count = sensor_count + 1
                        readings["eCO2"] = item
                        
    return readings
    #print("readings: {}".format(readings))


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
    
    if not bar_graph and not matrix_display:
        #print("Nothing to display on...")
        return

    if bar_graph:
        logger.debug("Skipping LED matrix display...")
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

    display_led(matrix2, right_digit, my_color)
    display_led(matrix1, left_digit, my_color)
    
def display_led(my_matrix, my_value, color):
    #
    # Display a single digit
    
    if not matrix_display:
        #print("Nothing to display on...")
        return

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
    #  Uses icons list 0,1=PM1; 2,3=PM2; 4,5=CO2
    
    if not matrix_display:
        #print("Nothing to display on...")
        return
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
    display_icon(icon_index, my_color)
    
    
def display_icon(icon_index, my_color):
    #
    # Display a two character icon on the display
    # icon_index is the index of the first character
    #
    if matrix_display:
    # Loop through digits from 1 to 0
        for digit in range(1, -1, -1):
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

def bar_index(idx):
    #
    # Display an index on the LED bargraph
    # idx = 0 - 99
    # bar color chosen by green_limit, yellow_limit
    #
    
    if not bar_graph:
        return
    try:
        my_stick.set_all_LED_brightness(1)
    except Exception as e:
        logger.error("Trouble communicating with LED: {}".format(e))
    j = 0
    for i in range(7,-1,-1):
        time.sleep(0.25)
        j = j + 1
        seg_value_start = (j-1) * (100/8)
        seg_value_end = j * (100/8)
        if bar_mode == 2: # All LEDs same color
            if idx <= green_limit:
                my_single_LED(my_stick, i, 0, 255, 0)
            elif idx > yellow_limit:
                my_single_LED(my_stick, i, 255, 0, 0)
            else:
                my_single_LED(my_stick, i, 255, 155, 0)
        else:  # Standard bargraph
            if ((idx > seg_value_start ) and (idx <= seg_value_end)) or (idx > seg_value_end):
                if idx <= green_limit:
                    my_single_LED(my_stick, i, 0, 255, 0)
                elif idx > yellow_limit:
                    my_single_LED(my_stick, i, 255, 0, 0)
                else:
                    my_single_LED(my_stick, i, 255, 155, 0)
            else:
                if bar_mode == 1: # Fill empty segments with white (default)
                    my_single_LED(my_stick, i, 25, 25, 25)
                else:  # Turn off empty segments
                    my_single_LED(my_stick, i, 0, 0, 0)

    # Turn on first segment if idx <= 12.5 and ZERO_BAR
    if (idx <= (100/8)) and (zero_bar == 1):
        #my_stick.set_single_LED_color(7, 0, 255, 0)
        my_single_LED(my_stick, 7, 0, 255, 0)

def LED_icon(icon_num):

    # Displays rudimentary animation on LED bar graph.

    if icon_num == 1:
        # alt red/grn
        my_single_LED(my_stick, 7, 255, 0, 0)
        time.sleep(0.2)
        my_single_LED(my_stick, 6, 0, 255, 0)
        time.sleep(0.2)
        my_single_LED(my_stick, 5, 255, 0, 0)
        time.sleep(0.2)
        my_single_LED(my_stick, 4, 0, 255, 0)
        time.sleep(0.2)
        my_single_LED(my_stick, 3, 255, 0, 0)
        time.sleep(0.2)
        my_single_LED(my_stick, 2, 0, 255, 0)
        time.sleep(0.2)
        my_single_LED(my_stick, 1, 255, 0, 0)
        time.sleep(0.2)
        my_single_LED(my_stick, 0, 0, 255, 0)
        time.sleep(0.2)

    if icon_num == 2:
        # All white
        my_single_LED(my_stick, 7, 25, 25, 25)
        time.sleep(0.2)
        my_single_LED(my_stick, 6, 25, 25, 25)
        time.sleep(0.2)
        my_single_LED(my_stick, 5, 25, 25, 25)
        time.sleep(0.2)
        my_single_LED(my_stick, 4, 25, 25, 25)
        time.sleep(0.2)
        my_single_LED(my_stick, 3, 25, 25, 25)
        time.sleep(0.2)
        my_single_LED(my_stick, 2, 25, 25, 25)
        time.sleep(0.2)
        my_single_LED(my_stick, 1, 25, 25, 25)
        time.sleep(0.2)
        my_single_LED(my_stick, 0, 25, 25, 25)
        time.sleep(0.2)

def my_single_LED(stick, a, b, c, d):

    # A wrapper for set_single_LED_color() with error checking
    
    try:
        stick.set_single_LED_color(a, b, c, d)
    except Exception as e:
        logger.error("Error accessing LED: {}".format(e))
        
            
############################ START ##############################


# startup LED animation
if bar_graph:
    LED_icon(2)

# Get a reading from the sensor block, see what measurements are available
reading = get_reading()
logger.info("initial reading: {}".format(reading))

# Make sure there's at least one sensor

if sensor_count < 1:
    if bar_graph:
        LED_icon(1)
        time.sleep(5)
    else:
        display_icon(8, 1)
    logger.critical("No sensors found! Exiting...")
    sys.exit()

if ("co2" not in reading) and ("eCO2" in reading):
    # Use eCO2 for CO2
    logger.info("Using eCO2 for CO2.")
    use_eco2 = True
            
# If using matrix LEDs, display sensor icons

if "pm10 standard" in reading:
    display_icon(0, 2)
    time.sleep(2)
    display_icon(2, 2)
    time.sleep(1)
   
if "TVOC" in reading:
    display_icon(6, 2)
    time.sleep(2)
        
if ("co2" in reading) or ("eCO2" in reading):
    display_icon(4, 2)
    time.sleep(1)

# Connect to internal MQTT for onboard dashboard

client = mqtt.Client()
try:
    client.connect("mqtt", 1883, 60)
except Exception as e:
    logger.error("Error connecting to internal mqtt. ({0})".format(str(e)))
else:
    client.loop_start()

# If set, connect to Aggregator (external)

if agg_address != "NONE":
    logger.debug("Preparing connection to external MQTT address {}".format(agg_address))
    client2 = mqtt.Client()

    if (agg_username is None) and (agg_password is None):
        logger.debug("Using external MQTT username ({}) and password.".format(agg_username))
        client2.username_pw_set(agg_username, agg_password)      
    try:
        client2.connect(agg_address, agg_port, 60)
    except Exception as e:
        logger.error("Error connecting to external mqtt. ({0})".format(str(e)))
    else:
        client2.loop_start()
    
while True:
    pm = {}
    scd = {}
    voc = {}
    if ("pm10 standard" in reading) and (reading["pm10 standard"] is not None):
        logger.info("Testimg PM...")
        pm10_idx = pm10_index(reading["pm100 env"])
        pm25_idx = pm25_index(reading["pm25 env"])
    if ("co2" in reading) and (reading["co2"] is not None):
        logger.info("Testing CO2...")
        co2_idx = co2_index(reading["co2"])
    if ("TVOC" in reading) and (reading["TVOC"] is not None):
        logger.info("Testing VOC...")
        voc_idx = voc_index(reading["TVOC"])
       
    if (use_eco2) and (reading["eCO2"] is not None):
        logger.info("Using eCO2 for CO2...")
        co2_idx = co2_index(reading["eCO2"])
        reading["co2"] = reading["eCO2"]
    else:
        if (use_eco2):
            logger.debug("No eCO2 reading found and use_eco2 is True.")

    logger.debug("Scaled pm25: {0}".format(pm25_idx))
    logger.debug("Scaled pm10: {0}".format(pm10_idx))
    logger.debug("Scaled co2: {0}".format(co2_idx))
    logger.debug("Scaled voc: {0}".format(voc_idx))  
    iaq_idx = max(pm25_idx, pm10_idx, co2_idx, voc_idx)
    # Add index to dict
    reading["IAQ"] = round(iaq_idx)
    logger.debug("Using index: {0}".format(iaq_idx))
    # Display on LED matrix
    display_index(iaq_idx)
    # Publish all data to internal MQTT
    try:
        client.publish("sensors/" + pretty_host_name, json.dumps(reading))
    except Exception as e:
        logger.error("Error publishing to internal mqtt. ({0})".format(str(e)))
    
    # Publish data to external MQTT
    ret = 0
    if agg_address != "NONE":
        agg_data["device"] = pretty_host_name
        agg_data["iaq"] = round(iaq_idx)
        agg_data["dominant"] = "tbd"
        logger.debug("Sending data {0} to external MQTT address {1}".format(agg_data, agg_address))
        try:
            ret = client2.publish("sensors/" + pretty_host_name, json.dumps(agg_data))
            logger.debug("Sent external mqtt data... topic: {0}; data: {1}; return: {2}".format("sensors/" + pretty_host_name, agg_data, ret))
        except Exception as e:
            logger.error("Error publishing to external mqtt. ({0})".format(str(e)))  
    else:
        logger.debug("No external MQTT address provided.")
                
    # Alternate display with icon every 2.5 seconds if index > green_limit
    if ((iaq_idx > alert_level) and (alert_mode == 1)) or (alert_mode == 2):
    #if (1 == 1):
        time.sleep(2.5)
        for recur in range(11):
            display_pollutant(pm10_idx, pm25_idx, co2_idx, voc_idx)
            time.sleep(2.5)
            display_index(iaq_idx)
            time.sleep(2.5)
    else:
        time.sleep(55)
    
    reading = get_reading()
    logger.info("loop reading: {}".format(reading))
