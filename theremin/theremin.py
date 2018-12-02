#!/usr/bin/python
import time
from volume import *
from pitch import *
import numpy as np

from pythonosc import osc_message_builder
from pythonosc import udp_client

if __name__ == "__main__":
	# setup udp
	client = udp_client.SimpleUDPClient("192.168.1.64",5105)

	# make instances for volume(ultrasonic ranger) and pitch (photo sensors)
	volume = Volume()
	pitch = Pitch()

	# we first calibrate volume
	# volume.calibrate()
	print('completed calibrating')
	while True:
		pr_1 = volume.volume1()
		pr_2 = volume.volume2()
		pr_3 = volume.volume3()
		pitch_value = pitch.pitchControl()

		print("---------------------------------------------------------")
		print("Low: "+str(volume.sensor1Low)+  "pr50: " +str(pr_1) + "pr30: "+ str(pr_2) + "pr20: "+str(pr_3) ) #"Pitch: "+str(pitch_value) )
		# Wait before repeating loop
		time.sleep(0.1)
		#msg = osc_message_builder.OscMessageBuilder(address = '/rpi/midi/values')
		#msg.add_arg('pr1', arg_type='s')
		#msg.add_arg(pr_1, arg_type='f')
		#msg.add_arg(volume.sensor1Low, arg_type='f')
		#msg.add_arg(volume.sensor1High, arg_type='f')
		#msg.add_arg('pr2', arg_type='s')
		#msg.add_arg(pr_2, arg_type='f')
		#msg.add_arg(volume.sensor2Low, arg_type='f')
		#msg.add_arg(volume.sensor2High, arg_type='f')
		#msg.add_arg('pr3', arg_type='s')
		#msg.add_arg(pr_3, arg_type='f')
		#msg.add_arg(volume.sensor3Low, arg_type='f')
		#msg.add_arg(volume.sensor3High, arg_type='f')

		# msg.add_arg('pitch', arg_type='s')
		# msg.add_arg(pitch_value, arg_type='f')
		#msg = msg.build()
		#client.send(msg)

		print("---------------------------------------------------------")

__main__()
