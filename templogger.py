#!/usr/bin/python3

# Can enable debug output by uncommenting:
#import logging
#logging.basicConfig(level=logging.DEBUG)

import time
import datetime
import Adafruit_MCP9808.MCP9808 as MCP9808
import os
import numpy as np

# Define a function to convert celsius to fahrenheit.
def c_to_f(c):
    return c * 9.0 / 5.0 + 32.0

def writeMeasurements(temp, file):
    opts = []
    firstLine = False
    if os.path.exists(file):
        opts = 'a'
    else:
        opts = 'w'
        firstLine = True

    meanTemp = np.mean(temp)
    maxTemp  = np.max(temp)
    minTemp  = np.min(temp)

    f = open(file, opts)
    if firstLine:
        f.write('epoch,datetime,min,mean,max,samples')

    t = time.time()
    l = time.localtime()
    strTime = time.asctime()
    outStr = '{0}, {1}, {2}, {3}, {4}, {5}\n'.format(t, strTime, minTemp, meanTemp, maxTemp, len(temp))
    f.write(outStr)
    f.close()


# Default constructor will use the default I2C address (0x18) and pick a default I2C bus.
#
# For the Raspberry Pi this means you should hook up to the only exposed I2C bus
# from the main GPIO header and the library will figure out the bus number based
# on the Pi's revision.
#
# For the Beaglebone Black the library will assume bus 1 by default, which is
# exposed with SCL = P9_19 and SDA = P9_20.
sensor = MCP9808.MCP9808()

# Optionally you can override the address and/or bus number:
#sensor = MCP9808.MCP9808(address=0x20, busnum=2)

# Initialize communication with the sensor.
sensor.begin()

temp = []
ltime = time.localtime()
old = ltime.tm_hour
while True:
    temp.append(sensor.readTempC())
    time.sleep(1.0)

    ltime = time.localtime()
    if ltime.tm_hour != old:
        old = ltime.tm_hour
        print('Saving measurement')
        writeMeasurements(temp, 'temp_measurements.csv')
        temp = []

