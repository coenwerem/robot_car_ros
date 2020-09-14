#!/usr/bin/env python

import rospy  # import roscpp for C++
#import numpy as np

import RPi.GPIO as GPIO
import time

from robot_car_ros.msg import ultRangerData
from robot_car_ros.msg import motorDriver
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
#from turtlesim.msg import Pose

GPIO.setmode(GPIO.BCM)

driverDetails = motorDriver()

#Available GPIO PINS on the Pi 3 are: 12, 13, 18, and 19.
driverDetails.ENABLE_A = 12
driverDetails.ENABLE_B = 18

driverDetails.dir1 = 13
driverDetails.dir2 = 19
driverDetails.dir3 = 20
driverDetails.dir4 = 16

# Initializing the duty cycle variables
driverDetails.minDutyCycle = 0
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

GPIO.setwarnings(False)

# Starting the PWM pins at 0% duty cycle
pwmA.start(driverDetails.minDutyCycle)
pwmB.start(driverDetails.minDutyCycle)

dc = driverDetails.dutyCycle = 0

def turnMotor(dc):
	pwmA.ChangeDutyCycle(dc)
	pwmB.ChangeDutyCycle(dc)


def forward(dc):
	turnMotor(dc)
	GPIO.output(driverDetails.dir1, True)
	GPIO.output(driverDetails.dir2, False)
	GPIO.output(driverDetails.dir3, True)
	GPIO.output(driverDetails.dir4, False)


def backward(dc):
	turnMotor(dc)
	GPIO.output(driverDetails.dir1, False)
	GPIO.output(driverDetails.dir2, True)
	GPIO.output(driverDetails.dir3, False)
	GPIO.output(driverDetails.dir4, True)


def stop():
	GPIO.output(driverDetails.dir1, False)
	GPIO.output(driverDetails.dir2, False)
	GPIO.output(driverDetails.dir3, False)
	GPIO.output(driverDetails.dir4, False)

#linArray = np.arange(-0.22, 0.22, 0.01)
#angArray = np.arange(-0.22, 0.22, 0.01)

def callback(msg):
	print("Velocity received.")

	prev_vel = msg.linear.x
	time.sleep(1)
	current_vel = msg.linear.x
	print("Previous Vel: %s") %prev_vel
	print("Current Vel: %s") %current_vel

	dc = abs(int(((msg.linear.x-prev_vel)/0.22)*driverDetails.maxDutyCycle))
	if msg.linear.x - prev_vel > 0:
		forward(dc)
		#print("Current Vel: %s") %msg.linear.x
		print("Robot moving forward.")
		prev_vel = msg.linear.x

	elif msg.linear.x - prev_vel < 0:
		backward(dc)
		print("Robot moving backward.")
		prev_vel = msg.linear.x

	else:
		stop()
		print("Robot stopped.")


def teleopRobot():

	rospy.init_node('driver', anonymous=True)
	rospy.Subscriber("/cmd_vel", Twist, callback)
	rospy.spin()


if __name__ == "__main__":

    try:

        teleopRobot()
	GPIO.cleanup()

    except KeyboardInterrupt:

	stop()

