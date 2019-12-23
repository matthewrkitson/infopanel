import logging
import logging.handlers

import gpiozero
import pygame

import signal
import os

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
        (14,  2, "media/bass_dnb_f.wav"),
        (15,  3, "media/elec_chime.wav"),
        (23,  4, "media/glitch_robot1.wav"),
#        (24, 17, ""),
#        (25, 27, ""),
#        ( 8, 22, ""),
#        ( 7, 10, ""),
#        (12,  9, "")
        ]

# buttons = { gpiozero.Button(btn): (gpiozero.LED(led), pygame.mixer.Sound(wav)) for (btn, led, wav) in gpio_pairs }
buttons = { gpiozero.Button(btn): (gpiozero.LED(led), wav) for (btn, led, wav) in gpio_pairs }

def handle_button_press(button):
    led, sound = buttons[button]
    logger.info("Button " + str(button) + "pressed, lighting LED " + str(led) + " and playing sound " + str(sound))
    led.on()
    # sound.play()
    os.system("aplay " + sound)
    led.off()

for button in buttons:
    button.when_pressed = handle_button_press

signal.pause()

logger.info("Information Panel stopping")
