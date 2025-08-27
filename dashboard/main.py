#!usr/bin/env python
import os
import logging
import signal
import serial
import asyncio
import threading
import time
import traceback
from dotenv import load_dotenv

import tkinter as tk
from tkinter import ttk

from gauge import GaugeCanvas 
from distance_widget import DistanceCanvas
from rectangle_dashboard_widget import RectangleDashboardCanvas

load_dotenv()

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)-7s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
_logger = logging.getLogger("dashboard")

WINDOW_WIDTH = int(os.getenv('DASHBOARD_WINDOW_WIDTH','500'))
WINDOW_HEIGHT = int(os.getenv('DASHBOARD_WINDOW_HEIGHT','500'))
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

def process_data():
    """
    Process data received from the serial port.

    This function reads data from the serial port and writes it to the log.

    It runs in an infinite loop until the application is stopped.

    :raises serial.SerialException: If there is an issue with the serial port
    :raises Exception: If there is an unexpected error
    """
    global running_app
    global serial_port

    counter = 0
    while running_app:
        try:
            data = serial_port.read(41)
            decoded_data = data.decode('utf-8', errors='replace').strip()
            decoded_data = decoded_data.replace('\r\n', '')
            decoded_data = decoded_data.replace('\x00', '')
            _logger.info(f"Received data: {decoded_data}")
            
            data_array = decoded_data.split(',')

            #_logger.info(data_array)

            security_distance.update_distances(front=int(float(data_array[0])), back=int(float(data_array[1])))
            dashboard_canvas.update_temperature_text(float(data_array[2]))
            dashboard_canvas.update_engine_temp_level(float(data_array[3])/100)
            rpm_gauge.update_value(int(data_array[4]) / 1000)
            speed_gauge.update_value(float(data_array[5]))
            dashboard_canvas.update_fuel_level(int(data_array[6])/255)
            dashboard_canvas.update_odometer(int(float(data_array[7])))
            

        except serial.SerialException as serial_error:
            _logger.error(f"Serial port error: {serial_error}")
            time.sleep(SLEEP_TIME_ON_ERROR)
            #await asyncio.sleep(SLEEP_TIME_ON_ERROR)
        except Exception as error:
            _logger.error(f"Unexpected error: {error}")
            _logger.error(traceback.format_exc())
            #time.sleep(SLEEP_TIME_ON_ERROR)
            #await asyncio.sleep(SLEEP_TIME_ON_ERROR)


def on_escape(event) -> None:
    """Closes the application when the Escape key is pressed."""
    os.kill(os.getpid(), signal.SIGTERM)

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
    global rpm_gauge
    global speed_gauge
    global security_distance
    global dashboard_canvas
    
    signal.signal(signal.SIGINT, handler_sigint)
    signal.signal(signal.SIGTERM, handler_sigint)

    _logger.info("Starting dashboard...")
    running_app = True

    serial_port = serial.Serial(port=SERIAL_PORT, baudrate=SERIAL_PORT_BAUDRATE, bytesize=SERIAL_PORT_BYTESIZE, parity=SERIAL_PORT_PARITY, stopbits=SERIAL_PORT_STOPBITS)
    
    # Window initialization
    window = tk.Tk()

    window.attributes('-topmost', True)
    window.bind('<Escape>', on_escape)

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    width_pos = int((screen_width / 2) - (WINDOW_WIDTH / 2))
    height_pos = int((screen_height / 2) - (WINDOW_HEIGHT / 2))

    window.title(WINDOW_TITLE)
    window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{width_pos}+{height_pos}")
    window.minsize(500, 10)

    rpm_gauge = GaugeCanvas(window, width=300, height=150, max_value=18, step=1)
    rpm_gauge.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    speed_gauge = GaugeCanvas(window, width=300, height=150, max_value=32, step=2)
    speed_gauge.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    security_distance = DistanceCanvas(window, width=150, height=200, front_distance=0, back_distance=0)
    security_distance.grid(row=0, column=2, rowspan=2, padx=10, pady=10, sticky="nsew")

    dashboard_canvas = RectangleDashboardCanvas(window, width=620, height=250)
    dashboard_canvas.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
    
    data_processing_thread = threading.Thread(target=process_data)
    
    data_processing_thread.start()

    window.mainloop()
    
    data_processing_thread.join()

if __name__ == '__main__':
    main()