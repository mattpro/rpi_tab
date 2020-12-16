#!/usr/bin/bash

cd /home/pi/Documents/rpi_tab
source venv/bin/activate
export FLASK_APP=main_web.py
flask run
