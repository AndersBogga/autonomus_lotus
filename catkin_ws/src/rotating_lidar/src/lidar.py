#!/usr/bin/env python
from __future__ import division, print_function
import rospy
import time
import smbus
from tfmini import TFmini
from std_msgs.msg import Float32

bus = smbus.SMBus(1)       				# 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)
DEVICE_ADDRESS = 0x36      				# 7 bit address (will be left shifted to add the read write bit)
tf = TFmini('/dev/ttyAMA0', mode=TFmini.STD_MODE)	# ttyAMA0 = hardware serial

def readAngle():	# Read angle value from AS5600
	bus.write_byte_data(DEVICE_ADDRESS, 0x0D, DEVICE_ADDRESS)
        bus.write_byte_data(DEVICE_ADDRESS, 0x0D, 0x1)
        position_angle = float((bus.read_word_data(DEVICE_ADDRESS, 0x0D)*360)/4096)
	return position_angle

def readDistance():	# Read distance value from TFmini lidar
	d = tf.read()
	if d:
		return d
	else:
		return -1

###############################################################################################
if __name__=='__main__':
	rospy.init_node('lidar')
	lidar = rospy.Publisher('lidar', Float32, queue_size=10)
	rate = rospy.Rate(5)

try:
	while not rospy.is_shutdown():
		lidar.publish(readDistance())
                lidar.publish(readAngle())
		time.sleep(0.01)

except KeyboardInterrupt:
	tf.close()

rate.sleep()
###############################################################################################
