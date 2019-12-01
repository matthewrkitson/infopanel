# infopanel
Raspberry Pi project to make a "museum-style" information panel with buttons that, when pressed light a light and play a recorded message. 

# Overview

* Raspberry Pi Zero W
 * Connected to LEDs through GPIO
 * With PWM0 and PWM1 redirected to GPIO 18 and GPIO 13
 * And a simple low pass filter connected to an audio amp and some speakers

# Raspberry Pi setup
* Download latest image and write to SD card. 

## On a Linux machine
```
  sudo su
  apt-get install funzip
  
  # Insert SD card
  dmesg 
  # Look at output to work out what device the SD card was recognised as
  
  # Download the latest raspbian image and unzip direct to the sd card 
  # (replace /dev/sdc with the appropriate device)
  wget -O - https://downloads.raspberrypi.org/raspbian_lite_latest | funzip > /dev/sdc
```
## On a Windows machine
* Downnload the image file: https://downloads.raspberrypi.org/raspbian_lite_latest
* Write to an SD card using [Etcher](https://www.balena.io/etcher/)

## Configure the SD card
* Copy the files from the [setup/boot] folder to the boot partiton
  * Add an empty file called `ssh` to the boot partition
  * Add a file called `wpa_supplicant.conf` to the boot partition, and fill with your WiFi settings

## Install the software
* Turn the Raspberry Pi on
* By default, it will appear on the network as "raspberrypi"
* Log in using the standard Raspbian username and password
* Configure the system by downloading the setup script and running it:
  * `curl https://raw.githubusercontent.com/matthewrkitson/infopanel/master/setup/setup.sh --output setup.sh && chmod +x setup.sh && ./setup.sh`
