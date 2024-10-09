#!usr/bin/env python
import os
import logging
import signal
import serial

import tkinter as tk
from tkinter import ttk

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)-7s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
_logger = logging.getLogger("dashboard")

WINDOW_SIZE = os.getenv('DASHBOARD_WINDOW_SIZE')
WINDOW_TITLE = os.getenv('DASHBOARD_WINDOW_TITLE')
SERIAL_PORT = os.getenv('CONNECTION_SERIAL_PORT')
SERIAL_PORT_BAUDRATE = os.getenv('CONNECTION_SERIAL_PORT_BAUDRATE')
SERIAL_PORT_BYTESIZE = os.getenv()
SERIAL_PORT_PARITY = os.getenv()
SERIAL_PORT_STOPBITS = os.getenv()

def handler_sigint(signum, frame) -> None:
    """Handle sigterm signals to close the app gracefully"""
    _logger.warning("Ctrl-c was pressed")
    _logger.warning("Application is going to be stopped at the end of the current iteration")
    global running_app

    running_app = False

def main() -> None:
    """"""
    global running_app
    global window 
    global serial_port
    
    
    signal.signal(signal.SIGINT, handler_sigint)
    signal.signal(signal.SIGTERM, handler_sigint)

    _logger.info("Starting dashboard...")
    running_app = True

    serial_port = serial.Serial(port=SERIAL_PORT, baudrate=SERIAL_PORT_BAUDRATE, bytesize=SERIAL_PORT_BYTESIZE, parity=SERIAL_PORT_PARITY, stopbits=SERIAL_PORT_STOPBITS)  

    window = tk.Tk()
    window.title(WINDOW_TITLE)
    window.geometry(WINDOW_SIZE)

if __name__ == '__main__':
    main()