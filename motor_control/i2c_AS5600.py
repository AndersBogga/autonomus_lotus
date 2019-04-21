#!/usr/bin/python

import smbus
from time import sleep

bus = smbus.SMBus(1)       # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

DEVICE_ADDRESS = 0x36      #7 bit address (will be left shifted to add the read write bit)

while(True):
	bus.write_byte_data(DEVICE_ADDRESS, 0x0D, DEVICE_ADDRESS)
	bus.write_byte_data(DEVICE_ADDRESS, 0x0D, 0x1) 			# R = high = 1
	position_angle = float((bus.read_word_data(DEVICE_ADDRESS, 0x0D)*360)/4096)

	bus.write_byte_data(DEVICE_ADDRESS, 0x0D, DEVICE_ADDRESS)
        bus.write_byte_data(DEVICE_ADDRESS, 0x0D, 0x1)                  # R = high = 1
        position_raw_angle = float((bus.read_word_data(DEVICE_ADDRESS, 0x0D)*360)/4096)


	print position_angle, position_raw_angle
