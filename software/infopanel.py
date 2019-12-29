import logging
import logging.handlers

import gpiozero
import pygame

import signal
import os
import pathlib
import itertools

logger = logging.getLogger(__name__)
fileHandler = logging.handlers.RotatingFileHandler("infopanel.log", maxBytes=1024*1024, backupCount=5)
logger.addHandler(fileHandler)
consoleHandler = logging.StreamHandler()
logger.addHandler(consoleHandler)
logger.setLevel(logging.DEBUG)
logger.info("Information Panel starting")

pygame.mixer.init()

# Pairs are GPIO pins of buttons and corresponding lights. 
gpio_pairs = [ 
        (14,  2),
        (15,  3),
        (23,  4),
        (24, 17, ""),
        (25, 27, ""),
        ( 8, 22, ""),
        ( 7, 10, ""),
        (12,  9, "")
        ]

# buttons = { gpiozero.Button(btn): (gpiozero.LED(led), pygame.mixer.Sound(wav)) for (btn, led, wav) in gpio_pairs }
buttons = { gpiozero.Button(btn): (gpiozero.LED(led), find_media(i)) for i, (btn, led) in enumerate(gpio_pairs) }

def find_media(index):
    boot_media_folder = pathlib.Path("/boot/media")
    boot_media_files = boot_media_folder.glob(str(index) + "*")

    local_media_folder = pathlib.Path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "media"))
    local_media_files = local_media_folder.glob(str(index) + "*")

    all_files = list(itertools.chain(boot_media_files, local_media_files))
    if len(all_files) > 0:
        return all_files[0]
    else:
        return None

def handle_button_press(button):
    led, sound = buttons[button]
    logger.info("Button " + str(button) + "pressed, lighting LED " + str(led) + " and playing sound " + str(sound))
    led.on()
    if sound:
        os.system("aplay " + sound)
    led.off()

for button in buttons:
    button.when_pressed = handle_button_press

signal.pause()

logger.info("Information Panel stopping")
