import spidev
import time
from threading import Thread

class Volume:
	def __init__(self): # Open SPI bus
		self.spi = spidev.SpiDev()
		self.spi.open(0,0)
		self.spi.max_speed_hz=1000000
		self.sensor1Low=3.3
		self.sensor1High=0
		self.sensor2Low=3.3
		self.sensor2High=0
		self.sensor3Low=3.3
		self.sensor3High=0
		self._running = False

	def terminate(self):
		self._running = True

	def aggVolume(self):
		volt1 = self.volume50()
		volt2 = self.volume30()
		volt3 = self.volume20()
		agg_volt = 0.5 * volt1 + 0.3 * volt2 + 0.2 * volt3
		# print('Aggregated Volume:' +str(agg_volt))
		return agg_volt

	def volume1(self): # Function to read SPI data from MCP3008 chip# Channel must be an integer 0-7
		adc50 = self.spi.xfer2([1,(8+2)<<4,0])
		pr50 = ((adc50[1]&3) << 8) + adc50[2]

		vol1 = round( (pr50 * 3.3) / float(1023),3)
		# volume50 = self.translate(volt50, self.sensor2Low, self.sensor2High)
		# print('Translated Real Volume 50%' +str(volume50))
		return vol1

	def volume2(self): # Function to read SPI data from MCP3008 chip# Channel must be an integer 0-7
		adc30 = self.spi.xfer2([1,(8+1)<<4,0])
		pr30 = ((adc30[1]&3) << 8) + adc30[2]

		vol2 = round( (pr30 * 3.3) / float(1023),3)
		# volume30 = self.translate(volt30, self.sensor1Low, self.sensor1High)
		# print('Translated Real Volume 30%' +str(volume30))
		return vol2

	def volume3(self):	# Function to read SPI data from MCP3008 chip# Channel must be an integer 0-7
		adc20 = self.spi.xfer2([1,(8+3)<<4,0])
		pr20 = ((adc20[1]&3) << 8) + adc20[2]

		vol3 = round( (pr20 * 3.3) / float(1023),3)
		# volume20 = self.translate(volt20, self.sensor3Low, self.sensor3High)
		# print('Translated Real Volume 20%' +str(volume20))
		return vol3

	# Function to conver volume to 0-100
	def translate(self,value,sensorLow,sensorHigh):
		# Figure out how 'wide' each range is
		leftSpan = sensorHigh-sensorLow
		rightSpan = 100
		# Convert the left range into a 0-1 range (float)
		valueScaled = float(value - sensorLow) / float(leftSpan)

		# Convert the 0-1 range into a value in the right range.
		return  (valueScaled * rightSpan)

	def calibrateVol(self,s):
                print(s)
                # Function to read SPI data from MCP3008 chip
                # Channel must be an integer 0-7
                adc = self.spi.xfer2([1,(8+s)<<4,0])
                pr = ((adc[1]&3) << 8) + adc[2]

                volt = round( (pr * 3.3) / float(1023),3)
                return volt

	def calibrate(self):
		time_end=time.time() + 5
		print('Calibration starts')

		# calibrate for the first five seconds after program runs
		while (time.time() < time_end):
			sensor1_30 = self.calibrateVol(1)
			sensor2_50 = self.calibrateVol(2)
			sensor3_20 = self.calibrateVol(3)
			print(str(sensor1_30) + " "+str(sensor2_50) + " " +str(sensor3_20) )
			try:
				if (sensor1_30 > self.sensor1High):								# record the maximum sensor value
					self.sensor1High = sensor1_30 									# record the minimum sensor value
				if (sensor1_30 < self.sensor1Low):
					self.sensor1Low = sensor1_30

				if (sensor2_50 > self.sensor2High):                                                              # record the maximum sensor value
					self.sensor2High = sensor2_50                                                                  # record the minimum sensor valu
				if (sensor2_50 < self.sensor2Low):
					self.sensor2Low = sensor2_50

				if (sensor3_20 > self.sensor3High):                                                              # record the maximum sensor value
					self.sensor3High = sensor3_20                                                                  # record the minimum sensor value
				if (sensor3_20 < self.sensor3Low):
					self.sensor3Low = sensor3_20
			except Exception as e:
				 print(str(e))
		print(str(self.sensor1Low) + ' '+str(self.sensor1High))
		print(str(self.sensor2Low) + ' '+str(self.sensor2High))
		print(str(self.sensor3Low) + ' '+str(self.sensor3High))
		print('Calibration ended');


