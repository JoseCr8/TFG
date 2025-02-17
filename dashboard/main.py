#!usr/bin/env python
import os
import logging
import signal
import serial
import asyncio
from dotenv import load_dotenv

import tkinter as tk
from tkinter import ttk

load_dotenv()

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)-7s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
_logger = logging.getLogger("dashboard")

WINDOW_SIZE = str(os.getenv('DASHBOARD_WINDOW_SIZE','500x500'))
WINDOW_TITLE = str(os.getenv('DASHBOARD_WINDOW_TITLE','CarInfo'))
SERIAL_PORT = str(os.getenv('CONNECTION_SERIAL_PORT'))
SERIAL_PORT_BAUDRATE = int(os.getenv('CONNECTION_SERIAL_PORT_BAUDRATE', '115200'))
SERIAL_PORT_BYTESIZE = int(os.getenv('CONNECTION_SERIAL_PORT_BYTESIZE', '8'))
SERIAL_PORT_PARITY = str(os.getenv('CONNECTION_SERIAL_PORT_PARITY', 'N'))
SERIAL_PORT_STOPBITS = int(os.getenv('CONNECTION_SERIAL_PORT_STOPBITS', '1'))
SLEEP_TIME_ON_ERROR = 1

def handler_sigint(signum, frame) -> None:
    """Handle sigterm signals to close the app gracefully"""
    _logger.warning("Ctrl-c was pressed")
    _logger.warning("Application is going to be stopped at the end of the current iteration")
    global running_app
    global serial_port

    serial_port.close()
    running_app = False

async def process_data():
    """
    Process data received from the serial port.

    This function reads data from the serial port and writes it to the log.

    It runs in an infinite loop until the application is stopped.

    :raises serial.SerialException: If there is an issue with the serial port
    :raises Exception: If there is an unexpected error
    """
    global running_app
    global serial_port

    while running_app:
        try:
            data = serial_port.read(30)
            decoded_data = data.decode('utf-8', errors='replace').strip()
            decoded_data = decoded_data.replace('\r\n', '')
            _logger.info(f"Received data: {decoded_data}")

        except serial.SerialException as serial_error:
            _logger.error(f"Serial port error: {serial_error}")
            await asyncio.sleep(SLEEP_TIME_ON_ERROR)
        except Exception as error:
            _logger.error(f"Unexpected error: {error}")
            await asyncio.sleep(SLEEP_TIME_ON_ERROR)
        
async def main_loop() -> None:
    """
    Main loop of the application."""
    async with asyncio.TaskGroup() as tg:
        serial_processing_task = tg.create_task(process_data())

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

    asyncio.run(main_loop())

if __name__ == '__main__':
    main()