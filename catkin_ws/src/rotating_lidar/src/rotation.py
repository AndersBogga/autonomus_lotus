#!/usr/bin/env python

import rospy
import time
import sys
import RPi.GPIO as GPIO
import math

from std_msgs.msg import Float32

GPIO.setmode(GPIO.BCM)

GPIO_Yaw   = [2,3,4,17]
for pin in GPIO_Yaw:
  GPIO.setup(pin,GPIO.OUT)
  GPIO.output(pin, False)

Seq = [[1,0,0,0],
       [1,1,0,0],
       [0,1,0,0],
       [0,1,1,0],
       [0,0,1,0],
       [0,0,1,1],
       [0,0,0,1],
       [1,0,0,1]]

SeqCount = len(Seq)
WaitTime = 2/float(1000)

# Stepper motor control for 28BYJ-48
 # Pins: What GPIO pins on the raspberry pi zero
 # StepLimit: 28BYJ-48 has a gear ratio of 63.68395. One full revolution takes 4074.7728 steps.
 # WaitTime: Time between each step, it is apparant when it is too quick since the motor will skip steps.
 # Direction: 1 = CW, -1 = CCW
 # Speed: 1 = Half step mode (slower), 2 = Full step mode (faster)
 # Name: The printed name of the motor
def step(Pins, StepLimit, WaitTime, Direction, Speed):
  Steps = 0
  SeqCounter = 0
  Angle = 0

  while Steps<=StepLimit:
    Steps = Steps + 1*Speed
    Angle = Steps*(360/4074.7728) 

    if Direction == -1:
      pub.publish(180-Angle)
    else:
      pub.publish(Angle)

    for pin in range(0, 4):
      pinx = Pins[pin]
      if Seq[SeqCounter][pin]!=0:
        GPIO.output(pinx, True)
      else:
        GPIO.output(pinx, False)

    SeqCounter = SeqCounter + (Direction*Speed)
 
    # If we reach the end of the pin sequence - start again
    if (SeqCounter>=SeqCount):
      SeqCounter = 0
    if (SeqCounter<0):
      SeqCounter = SeqCount+(Direction*Speed)

    # Wait before moving on
    time.sleep(WaitTime)

##########################################################################
##########################################################################
if __name__=='__main__':
    rospy.init_node('yaw_stepper')
    pub=rospy.Publisher('yaw_stepper', Float32, queue_size=10)
    rate= rospy.Rate(5)

try:
    while not rospy.is_shutdown():
      step(GPIO_Yaw, 4074/2, WaitTime, 1, 1)
      step(GPIO_Yaw, 4074/2, WaitTime, -1, 1)

except KeyboardInterrupt:
    tf.close()

rate.sleep()
##########################################################################
##########################################################################
