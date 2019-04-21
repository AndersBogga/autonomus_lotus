#!/usr/bin/env python
from __future__ import division, print_function
import rospy
import time
from tfmini import TFmini
from std_msgs.msg import Float32

tf = TFmini('/dev/ttyAMA0', mode=TFmini.STD_MODE)

if __name__=='__main__':
    rospy.init_node('tf_mini')
    pub=rospy.Publisher('tf_mini', Float32, queue_size=10)
    rate= rospy.Rate(5)

try:
    while not rospy.is_shutdown():
          d = tf.read()
          if d:
              pub.publish(d)
          else:
              pub.publish(-1)
          time.sleep(0.01)

except KeyboardInterrupt:
    tf.close()

rate.sleep()
