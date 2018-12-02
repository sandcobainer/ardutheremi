import RPi.GPIO as GPIO
import time
import sys
from range_key_dict import RangeKeyDict

class Pitch:
	def __init__(self):
		GPIO.setmode(GPIO.BOARD)
		self.PIN_TRIGGER = 7
		self.PIN_ECHO = 11
		self.samp =  10
		GPIO.setup(self.PIN_TRIGGER, GPIO.OUT)
		GPIO.setup(self.PIN_ECHO, GPIO.IN)
		self.summedtimes = 0
		self.pulse_begin = 0; self.pulse_end =  0
		self.avgdist = 0; self.sumdist = 0
		GPIO.output(self.PIN_TRIGGER, GPIO.LOW)
		self._running = True
	def terminate(self):
		self._running = False

	def pitchControl(self):
		self.summedtimes = 0
		try:
			for x in range(0, self.samp):
				GPIO.output(self.PIN_TRIGGER, GPIO.HIGH)
				time.sleep(0.000001)
				GPIO.output(self.PIN_TRIGGER, GPIO.LOW)
				while (GPIO.input(self.PIN_ECHO)==0):
					self.pulse_start_time = time.time();
				while (GPIO.input(self.PIN_ECHO)==1):
					self.pulse_end_time = time.time();
				self.pulse_duration = self.pulse_end_time - self.pulse_start_time
				self.summedtimes  = self.summedtimes + self.pulse_duration

			self.sumdist  = self.summedtimes * 34300 * 0.5
			self.avgdist = round((self.sumdist/self.samp),1)
			print(self.avgdist)
			return self.avgdist
		except Exception as e:
			print(str(e))


