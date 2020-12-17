#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://max7219.readthedocs.io/en/0.2.3/


import time
import argparse
import pygame
from datetime import datetime
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.legacy import show_message
from luma.core.legacy import text
from luma.core.legacy.font import proportional, CP437_FONT, LCD_FONT, SEG7_FONT, SINCLAIR_FONT, TINY_FONT, UKR_FONT
from luma.core.render import canvas

#Do SPI0 podłączony jest wyświetlacz z pływajacym tekstem + zegar
serial0 = spi(port=0, device=0, gpio=noop())
device0 = max7219(serial0, cascaded= 8, block_orientation=90,
				 rotate=2, blocks_arranged_in_reverse_order=True)

#Do SPI1 podłączony jest wyświetlacz z licznikiem zgonów i dni bez wypadku 
serial1 = spi(port=0, device=1, gpio=noop())
device1 = max7219(serial1, cascaded= 8, block_orientation=90,
				 rotate=2, blocks_arranged_in_reverse_order=True)

				 
def printDaysWithoutDie(daysWithoutDie, recorDaysWithoutDie ):
	with canvas(device1) as draw:
		text(draw, (0, 0), "%5d  %5d" % (daysWithoutDie, recorDaysWithoutDie), fill="white", font=proportional(LCD_FONT))


def printDateAndTime(dateTime):
	#current_time = now.strftime("%d.%m.%y  %H:%M:%S")
	current_time = dateTime.strftime("   %H:%M:%S  ")
	with canvas(device0) as draw:
		text(draw, (0, 0), current_time, fill="white", font=proportional(LCD_FONT))	

def printCustomMessage(message):
	show_message(device0, message, fill="white", font=proportional(LCD_FONT), scroll_delay=0.05)
	

def playBarka():
	pygame.mixer.init()
	pygame.mixer.music.load("barka.mp3")
	pygame.mixer.music.set_volume(1.0)
	pygame.mixer.music.play()

	while pygame.mixer.music.get_busy() == True:
		pass
	
newMessageFlag = False
	

import simpleaudio as sa

def playBarka2():	
	wave_obj = sa.WaveObject.from_wave_file("barka.wav")
	play_obj = wave_obj.play()
	play_obj.wait_done()



#COMPANY_START = datetime.date(2019, 5, 1)



#playBarka()
playBarka2()
				 
while 0:
	now = datetime.now()
	current_time = now.strftime("%d.%m.%Y %H:%M:%S")
	print(current_time)
	printDaysWithoutDie(678, 897)
	time.sleep(0.5)
	#if now.hour = 21 and now.min = 37:
	if now.hour == 23 and now.min == 25:
		playBarka()
		printCustomMessage("Pokolenie JP2")
	elif newMessageFlag:
		newMessageFlag = False
		printCustomMessage("Jakas wiadomosc do wyswietlenia")
	else:
		printDateAndTime(now)
	
	time.sleep(0.5)
				



