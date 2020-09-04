#!/usr/bin/env python

import rospy  # import roscpp for C++

import RPi.GPIO as GPIO
import time

from robot_car_ros.msg import ultRangerData
from robot_car_ros.msg import motorDriver
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

GPIO.setmode(GPIO.BCM)

driverDetails = motorDriver()

# Available GPIO PINS on the Pi 3 are: 12, 13, 18, and 19.
driverDetails.ENABLE_A = 12
driverDetails.ENABLE_B = 18

driverDetails.dir1 = 13
driverDetails.dir2 = 19
driverDetails.dir3 = 20
driverDetails.dir4 = 16

# Initializing the duty cycle variables
driverDetails.minDutyCycle = 1
driverDetails.maxDutyCycle = 100

GPIO.setup(driverDetails.ENABLE_A, GPIO.OUT)
GPIO.setup(driverDetails.ENABLE_B, GPIO.OUT)
GPIO.setup(driverDetails.dir1, GPIO.OUT)
GPIO.setup(driverDetails.dir2, GPIO.OUT)
GPIO.setup(driverDetails.dir3, GPIO.OUT)
GPIO.setup(driverDetails.dir4, GPIO.OUT)

GPIO.output(driverDetails.ENABLE_A, True)
GPIO.output(driverDetails.ENABLE_B, True)

# Creating an object of the pwm pins
pwmA = GPIO.PWM(driverDetails.ENABLE_A, 100)
pwmB = GPIO.PWM(driverDetails.ENABLE_B, 100)

# Starting the PWM pins at 0% duty cycle
pwmA.start(0)
pwmB.start(0)

def forward():
    GPIO.output(driverDetails.dir1, True)
    GPIO.output(driverDetails.dir2, False)
    GPIO.output(driverDetails.dir3, True)
    GPIO.output(driverDetails.dir4, False)


def backward():
    GPIO.output(driverDetails.dir1, False)
    GPIO.output(driverDetails.dir2, True)
    GPIO.output(driverDetails.dir3, False)
    GPIO.output(driverDetails.dir4, True)


def stop():
    GPIO.output(driverDetails.dir1, False)
    GPIO.output(driverDetails.dir2, False)
    GPIO.output(driverDetails.dir3, False)
    GPIO.output(driverDetails.dir4, False)


def callback(data):
    for i in range (minDutyCycle, maxDutyCycle, 5):
        for Pose.linear_velocity in range(0, 2):
            GPIO.ChangeDutyCycle(50)
            time.sleep(0.1)
    
        rospy.loginfo(data.linear.x)
        backward()
        #time.sleep(3)
        #stop()

    else:
        rospy.loginfo(data.distance)
        forward()
        #time.sleep(3)
        #stop()


def receiveDistance():

    rospy.init_node('driver', anonymous=True)
    rospy.Subscriber("/turtle1/cmd_vel", Twist, callback)
    rospy.spin()  # This keeps Python form exiting until the node is stopped


if __name__ == "__main__":

    try:

        receiveDistance()

    except rospy.ROSInterruptException:

        stop()
