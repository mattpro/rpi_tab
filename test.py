#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://max7219.readthedocs.io/en/0.2.3/


import time
import argparse

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.legacy import show_message
from luma.core.legacy import text
from luma.core.legacy.font import proportional, CP437_FONT
from luma.core.render import canvas

serial = spi(port=0, device=0, gpio=noop())

device = max7219(serial, cascaded= 8, block_orientation=90,
				 rotate=0, blocks_arranged_in_reverse_order=True)
print("sdiodosdssd")


#show_message(device, "Co dzisiaj w sielanie?!?!", fill="white", font=proportional(CP437_FONT), scroll_delay=0)




with canvas(device) as draw:
    text(draw, (32, 0), "COstam", fill="white", font=proportional(CP437_FONT))

time.sleep(2)




def output(n, block_orientation, rotate, inreverse, text):
    # create matrix device
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=n or 1, block_orientation=block_orientation,
                     rotate=rotate or 0, blocks_arranged_in_reverse_order=inreverse)
    print(text)

    show_message(device, text, fill="white", font=proportional(CP437_FONT), scroll_delay=0.05)
    time.sleep(1)


#if __name__ == "__main__":
##    parser = argparse.ArgumentParser(description='view_message arguments',
#        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
#
#    parser.add_argument('--cascaded', '-n', type=int, default=1, help='Number of cascaded MAX7219 LED matrices')
#    parser.add_argument('--block-orientation', type=int, default=0, choices=[0, 90, -90], help='Corrects block orientation when wired vertically')
#    parser.add_argument('--rotate', type=int, default=0, choices=[0, 1, 2, 3], help='Rotate display 0=0Â°, 1=90Â°, 2=180Â°, 3=270Â°')
#    parser.add_argument('--reverse-order', type=bool, default=False, help='Set to true if blocks are in reverse order')
#    parser.add_argument('--text', '-t', default='>>> No text set', help='Set text message')
#    args = parser.parse_args()

#    try:
#        output(args.cascaded, args.block_orientation, args.rotate, args.reverse_order, args.text)
#    except KeyboardInterrupt:
#        pass
