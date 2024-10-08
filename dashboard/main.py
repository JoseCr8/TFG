#!usr/bin/env python
import os
import logging
import signal

import tkinter as tk
from tkinter import ttk

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)-7s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
_logger = logging.getLogger("dashboard")

WINDOW_SIZE = os.getenv('DASHBOARD_WINDOW_SIZE')
WINDOW_TITLE = os.getenv('DASHBOARD_WINDOW_TITLE')

def handler_sigint(signum, frame) -> None:
    """Handle sigterm signals to close the app gracefully"""
    _logger.warning("Ctrl-c was pressed")
    _logger.warning("Application is going to be stopped at the end of the current iteration")
    global running_app

    running_app = False

def main():
    """"""
    global window 
    global running_app

    signal.signal(signal.SIGINT, handler_sigint)
    signal.signal(signal.SIGTERM, handler_sigint)

    _logger.info("Starting dashboard...")
    running_app = True

    window = tk.Tk()
    window.title(WINDOW_TITLE)
    window.geometry(WINDOW_SIZE)

if __name__ == '__main__':
    pass