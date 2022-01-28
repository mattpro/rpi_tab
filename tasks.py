import time
# import pygame
from datetime import datetime
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.legacy import show_message
from luma.core.legacy import text
from luma.core.legacy.font import proportional, CP437_FONT, LCD_FONT, SEG7_FONT, SINCLAIR_FONT, TINY_FONT, UKR_FONT
from luma.core.render import canvas
import simpleaudio as sa
import pyownet
import csv
from pyownet.protocol import OwnetTimeout
from threading import Timer
import time
import unicodedata

conclusiveStart = datetime(year=2019, month=5, day=1, hour=0, minute=0, second=0)

# Do SPI0 podłączony jest wyświetlacz z pływajacym tekstem + zegar
serial0 = spi(port=0, device=0, gpio=noop(), bus_speed_hz=500000, transfer_size=64, reset_hold_time=0.15, reset_release_time=0.15)
device0 = max7219(serial0, cascaded=8, block_orientation=90, rotate=2, blocks_arranged_in_reverse_order=True)
device0.contrast(208)

# Do SPI1 podłączony jest wyświetlacz z licznikiem zgonów i dni bez wypadku
serial1 = spi(port=0, device=1, gpio=noop(), bus_speed_hz=500000, transfer_size=64, reset_hold_time=0.15, reset_release_time=0.15)
device1 = max7219(serial1, cascaded=8, block_orientation=90, rotate=2, blocks_arranged_in_reverse_order=True)
device1.contrast(208)

owproxy = pyownet.protocol.proxy(host="localhost", port=4304)

class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFKD', text) if unicodedata.category(c) != 'Mn')

class LEDDisplay:
    def __init__(self) -> None:
        super().__init__()
        self.shown_text = 'EMPTY'
        self.newMessageFlag = False
        self.playSound = False
        self.last_temp = 0.0

    def getTemperature(self):
        try:
            temp_raw = owproxy.read('/28.126DC11E1901/temperature', timeout=1)
            if temp_raw:
                self.last_temp = float(temp_raw.decode("utf-8").strip())
                print("TEMP OK:"+str(datetime.now())+str(self.last_temp))
        except OwnetTimeout:
            print("TIMEOUT!")

    def logTemperatureToFile(self):
        fields=[datetime.now(), self.last_temp]
        with open(r'temperature_log.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(fields)

    def printDaysWithoutDie(self, daysWithoutDie, recorDaysWithoutDie):
        with canvas(device1) as draw:
            draw.rectangle([0, 0, device1.width, device1.height], fill="black")
            text(draw, (0, 0), "%5d  %5d" % (daysWithoutDie, recorDaysWithoutDie), 
            fill="white", font=proportional(LCD_FONT))

    def printDateAndTime(self, dateTime):
        current_time = dateTime.strftime("    %H:%M:%S  ")
        with canvas(device0) as draw:
            draw.rectangle([0, 0, device0.width, device0.height], fill="black")
            text(draw, (0, 0), current_time, fill="white", font=proportional(LCD_FONT))	

    def printCustomMessage(self, message):
        show_message(device0, strip_accents(message), fill="white", font=proportional(LCD_FONT), scroll_delay=0.05)

    # def playBarka():
    #     if pygame.mixer.music.get_busy() == False:
    #         pygame.mixer.init()
    #         pygame.mixer.music.load("barka.mp3")
    #         pygame.mixer.music.set_volume(1.0)
    #         pygame.mixer.music.play()

    def playBarka2(self):	
        wave_obj = sa.WaveObject.from_wave_file("barka.wav")
        play_obj = wave_obj.play()
        # play_obj.wait_done()

    def printTemperature(self):
        temp_text = "Temp. {:.1f} C".format(self.last_temp)
        with canvas(device0) as draw:
            draw.rectangle([0, 0, device0.width, device0.height], fill="black")
            text(draw, (0, 0), temp_text, fill="white", font=proportional(LCD_FONT))

    def tasks_change_text(self, new_text):
        self.shown_text = new_text
        self.newMessageFlag = True
        
    def threaded_rest(self):
        self.getTemperature()
        while True:
            now = datetime.now()
            detltaT = now - conclusiveStart
            self.printDaysWithoutDie(detltaT.days, detltaT.days)
                    
            if now.hour == 21 and now.minute == 37:
                if self.playSound == False:
                    self.playSound = True
                    self.playBarka2()
                self.printCustomMessage("Pokolenie JP2")
            elif self.newMessageFlag  == True:
                self.newMessageFlag  = False
                self.printCustomMessage(self.shown_text)
                self.printCustomMessage(self.shown_text)
            elif (now.second == 30) or (now.second == 0):
                self.printTemperature()
                time.sleep(5)
            else:
                self.printDateAndTime(now)

            if now.hour == 10 and now.minute == 14:
                self.playSound = False
            time.sleep(0.1)

if __name__ == "__main__":
    ld = LEDDisplay()
    backgroundThreads = [RepeatTimer(30, ld.getTemperature), RepeatTimer(900, ld.logTemperatureToFile)] 
    for t in backgroundThreads:
        t.start()
    ld.threaded_rest()
    for t in backgroundThreads:
        t.cancel()
