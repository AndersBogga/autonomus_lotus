#!/usr/bin/env python
from __future__ import division, print_function
import rospy
import time
import smbus
import math
from tfmini import TFmini
import std_msgs.msg
from sensor_msgs.msg import PointCloud
from geometry_msgs.msg import Point32

bus = smbus.SMBus(1)                                    # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)
DEVICE_ADDRESS = 0x36                                   # 7 bit address (will be left shifted to add the read write bit)
tf = TFmini('/dev/ttyAMA0', mode=TFmini.STD_MODE)       # ttyAMA0 = hardware serial

def readAngle():        # Read angle value from AS5600
        bus.write_byte_data(DEVICE_ADDRESS, 0x0D, DEVICE_ADDRESS)
        bus.write_byte_data(DEVICE_ADDRESS, 0x0D, 0x1)
        position_angle = float((bus.read_word_data(DEVICE_ADDRESS, 0x0D)*360)/4096)
        return position_angle

def readDistance():     # Read distance value from TFmini lidar
        d = tf.read()
        if d:
                return d
        else:
                return -1

###############################################################################################
if __name__=='__main__':
        rospy.init_node('pointcloud')
        pointcloud_pub = rospy.Publisher('/pointcloud', PointCloud, queue_size=10)
        rospy.sleep(0.5)
	lidar_pointcloud = PointCloud()
	header = std_msgs.msg.Header()
	rate = rospy.Rate(5)

try:
        while not rospy.is_shutdown():
		a = readAngle()
		c = readDistance()
		y = math.sin(math.radians(a))*c
		x = math.cos(math.radians(a))*c
		z = 0.0

		header.stamp = rospy.Time.now()
        	header.frame_id = 'map'
        	lidar_pointcloud.header = header

		lidar_pointcloud.points.append(Point32(x, y, z))
                pointcloud_pub.publish(lidar_pointcloud)
                time.sleep(0.01)

except KeyboardInterrupt:
        tf.close()

rate.sleep()
###############################################################################################

