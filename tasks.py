import time
import pygame
from datetime import datetime
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.legacy import show_message
from luma.core.legacy import text
from luma.core.legacy.font import proportional, CP437_FONT, LCD_FONT, SEG7_FONT, SINCLAIR_FONT, TINY_FONT, UKR_FONT
from luma.core.render import canvas
import simpleaudio as sa

conclusiveStart = datetime(year = 2019, month = 5, day = 1, hour = 0, minute = 0, second = 0)

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
	current_time = dateTime.strftime("    %H:%M:%S  ")
	with canvas(device0) as draw:
		text(draw, (0, 0), current_time, fill="white", font=proportional(LCD_FONT))	

def printCustomMessage(message):
	show_message(device0, message, fill="white", font=proportional(LCD_FONT), scroll_delay=0.05)
	

def playBarka():
    if pygame.mixer.music.get_busy() == False:
        pygame.mixer.init()
        pygame.mixer.music.load("barka.mp3")
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play()

def playBarka2():	
	wave_obj = sa.WaveObject.from_wave_file("barka.wav")
	play_obj = wave_obj.play()
	#play_obj.wait_done()




class LEDDisplay:
    def __init__(self) -> None:
        super().__init__()
        self.shown_text = 'EMPTY'
        self.newMessageFlag = False
        self.playSound = False

    def tasks_change_text(self, new_text):
        self.shown_text = new_text
        self.newMessageFlag = True
        
    def threaded_rest(self,):
        while True:
            now = datetime.now()
            detltaT = now - conclusiveStart
            printDaysWithoutDie(detltaT.days, detltaT.days)
            time.sleep(0.5)
                      
            if now.hour == 21 and now.minute == 37:
                if self.playSound == False:
                    self.playSound = True
                    playBarka2()
                printCustomMessage("Pokolenie JP2")        
            elif self.newMessageFlag  == True:
                self.newMessageFlag  = False
                printCustomMessage(self.shown_text)
            else:
                printDateAndTime(now)

            if now.hour == 10 and now.minute == 14:
                self.playSound = False
                
            time.sleep(0.5)