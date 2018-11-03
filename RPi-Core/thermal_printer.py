#!/usr/bin/python

import serial
import random
from Adafruit_Thermal import *

#SEE: https://github.com/adafruit/Python-Thermal-Printer
class ThermalPrinter:	

	def __init__(self, photo_data = None, image_width = 0, image_height = 0):
		self.photo_data = photo_data
		self.photo_width = image_width
		self.photo_height = image_height

	def generateRandomNumber(self, digits):
		number = ""
		for x in range(0, digits):
			number += str(random.randint(1, 9))
		return number

	def printLine(self, line, justify = 'L', fontSize = 'S', bold = False, underline = False, feed = 0):
	
		if(bold): 
			self.printer.boldOn()
		if(underline): 
			self.printer.underlineOn()

		self.printer.justify(justify)
		self.printer.setSize(fontSize)
		self.printer.println(line)
		self.printer.boldOff()
		self.printer.underlineOff()

		if(feed > 0):
			self.printer.feed(feed)

	def printReceipt(self, fee):	
		self.printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)
		self.printData(fee.age, fee.makeup, fee.pyjama, fee.hipster, fee.youngster, fee.oldie, fee.badMood, fee.aggressive)
		self.printer.sleep()      # Tell printer to sleep
		self.printer.wake()       # Call wake() before printing again, even if reset
		self.printer.setDefault() # Restore printer to defaults
		
	def formattedCurrency(self,number):
		if(number < 10):
			return "  " + str(number);
		if(number < 100): 
			return " " + str(number);
		return str(number)

	def printData(self, age, makeupFee, pyjamaFee, hipsterFee, youngsterFee, oldieFee, badMoodFee, aggressiveFee):
		#Print logo
		import gfx.logo as logo
		self.printer.printBitmap(logo.width, logo.height, logo.data)
		self.printLine("BRUTUS", 'C', 'L', True, False, 1)

		#Print photo
		if self.photo_data is not None:
			self.printer.printBitmap(self.photo_width, self.photo_height, self.photo_data)
		
		self.printer.feed(1)
		self.printer.setLineHeight(36)

		baseFee = 8
		totalFee = baseFee + makeupFee + pyjamaFee + hipsterFee + youngsterFee + oldieFee + badMoodFee + aggressiveFee

		#Print Content
		self.printLine("Estimated age                " + str(age), 'L', 'S', True)
		self.printLine("Base Fee                EUR " + self.formattedCurrency(baseFee), 'L', 'S', False, False, 1)
		
		self.printLine("Appearance Cost", 'L', 'S', True)
		self.printLine("No-Make-Up Fee          EUR " + self.formattedCurrency(makeupFee))
		self.printLine("Underdressed Fee        EUR " + self.formattedCurrency(pyjamaFee))
		self.printLine("Hipster Fee             EUR " + self.formattedCurrency(hipsterFee))
		self.printer.feed(1)

		self.printLine("General Cost", 'L', 'S', True)
		self.printLine("Youngster Fee           EUR " + self.formattedCurrency(youngsterFee))
		self.printLine("Oldie Fee               EUR " + self.formattedCurrency(oldieFee))
		self.printLine("Bad Mood Fee            EUR " + self.formattedCurrency(badMoodFee))	
		self.printLine("Aggressive Behavior Fee EUR " + self.formattedCurrency(aggressiveFee))
		self.printer.feed(1)

		#Print Total
		self.printLine("Total                   EUR " + self.formattedCurrency(totalFee), 'L', 'S', True, True, 1)	

		#Print Barcode	
		self.printer.setBarcodeHeight(100)
		number = self.generateRandomNumber(13)		
		self.printer.printBarcode(number, self.printer.EAN13)	

		self.printer.feed(2)
