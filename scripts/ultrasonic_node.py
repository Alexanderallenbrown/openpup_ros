#!/usr/bin/env python

import RPi.GPIO as gpio
import time
from numpy import *
import sys
import signal
from std_msgs.msg import Float32

import rospy
import roslib
roslib.load_manifest('openpup_ros')

# ---------------
# ULTRASONIC NODE
# ---------------

# this node reads the ultrasonic signal and calculates the distance based on
# the time between sending and receiving a pulse

def signal_handler(signal, frame): # ctrl + c -> exit program
		print('You pressed Ctrl+C!')
		sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


class sonar():

	def __init__(self):
		rospy.init_node('sonar', anonymous=True)
		self.distance_publisher = rospy.Publisher('/sonar_dist',Float32, queue_size=1)
		self.r = rospy.Rate(15)

	def dist_sensor(self,dist):
		data = Float32()
		data.data = dist
		self.distance_publisher.publish(data)


gpio.setmode(gpio.BCM)
trig = 4
echo = 17

gpio.setup(trig, gpio.OUT)
gpio.setup(echo, gpio.IN)

sensor = sonar()
time.sleep(0.5)
print ('--sonar start--')

try :
	while True :
		#print('running')
		gpio.output(trig, False)
		time.sleep(0.1)
		gpio.output(trig, True)
		time.sleep(0.00001)
		gpio.output(trig, False)

		while gpio.input(echo) == 0 :
			pulse_start = time.time()
			#print('no')

		while gpio.input(echo) == 1 :
			pulse_end = time.time()
			#print('yes')

		pulse_duration = pulse_end - pulse_start
		distance = pulse_duration * 17000
		distance = round(distance, 3)

		if pulse_duration >= 0.01746:
			#print('time out')
			distance = float("inf")
			continue

		elif distance > 300 or distance == 0:
			#print('out of range')
			distance = float("inf")
			continue

		#print ('Distance : %f cm'%distance)
		sensor.dist_sensor(distance)

		sensor.r.sleep()


except (KeyboardInterrupt, SystemExit):
	gpio.cleanup()
	sys.exit(0)
except:
	gpio.cleanup()
