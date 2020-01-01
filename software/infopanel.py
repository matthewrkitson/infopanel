import logging
import logging.handlers

import gpiozero

import signal
import os
import pathlib
import itertools

logger = logging.getLogger(__name__)

fileHandler = logging.handlers.RotatingFileHandler("infopanel.log", maxBytes=1024*1024, backupCount=5)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
logger.addHandler(consoleHandler)

formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
consoleHandler.setFormatter(formatter)
fileHandler.setFormatter(formatter)

logger.setLevel(logging.DEBUG)
logger.info("Information Panel starting")

# Pairs are GPIO pins of buttons and corresponding lights. 
gpio_pairs = [ 
        (14,  2),
        (15,  3),
        (23,  4),
        (24, 17),
        (25, 27),
        ( 8, 22),
        ( 7, 10),
        (12,  9)
        ]

def find_media(index):
    boot_media_folder = pathlib.Path("/boot/media")
    boot_media_files = boot_media_folder.glob(str(index + 1) + "*")

    local_media_folder = pathlib.Path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "media"))
    local_media_files = local_media_folder.glob(str(index + 1) + "*")

    all_files = list(itertools.chain(boot_media_files, local_media_files))
    if len(all_files) > 0:
        return str(all_files[0])
    else:
        return None

def handle_button_press(button):
    led, sound, audio = buttons[button]
    logger.info("Button " + str(button) + "pressed, lighting LED " + str(led) + " and playing sound " + str(sound))
    led.on()
    audio.on()
    if sound:
        os.system("aplay '" + sound + "'")
    led.off()
    audio.off()
    logger.info("Done")

audio = gpiozero.DigitalOutputDevice(16, active_high=False)
audio.off()

buttons = { gpiozero.Button(btn): (gpiozero.LED(led), find_media(i), audio) for i, (btn, led) in enumerate(gpio_pairs) }

for button in buttons:
    button.when_pressed = handle_button_press

signal.pause()

logger.info("Information Panel stopping")
