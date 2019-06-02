#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from neopixel import *
import argparse
from flask import Flask
import random
import RPi.GPIO as GPIO


app = Flask(__name__)

# LED strip configuration:
LED_COUNT = 60      # Number of LED pixels.
LED_PIN = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Button Pin Configuration
ButtonPin = 24
# Set Led status to True(OFF)
Led_status = True


leds = {
    'red': (0, 255, 0),
    'blue': (0, 0, 255),
    'green': (255, 0, 0)
}

userColor = [0]

usedColorStrip = {

}

print(ButtonPin)
print(LED_PIN)

#
# Define a setup function for some setup


def setup():
	# Set the GPIO modes to BCM Numbering
	GPIO.setmode(GPIO.BCM)
	# Set LedPin's mode to output,
	# and initial level to high (3.3v)
	#GPIO.setup(LedPin, GPIO.OUT, initial=GPIO.HIGH)
	# Set BtnPin's mode to input,
	# and pull up to high (3.3V)
	GPIO.setup(ButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	# Set up a falling detect on BtnPin,
	# and callback function to swLed
	GPIO.add_event_detect(ButtonPin, GPIO.FALLING, callback=swLed)

# Define a callback function for button callback


def swLed(ev=None):
    global Led_status
    # Switch led status(on-->off; off-->on)
    Led_status = not Led_status
    #GPIO.output(Led_status)
    if Led_status:
        print('LED OFF')
    else:
        print('LED ON')
        randomG = random.randint(0, 255)
        randomR = random.randint(0, 255)
        randomB = random.randint(0, 255)
        #print(randomColor)
        print("userColor?")
        print(userColor)
        setRandomColor(strip, Color(randomG, randomR, randomB))
#


# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    userColor.pop(0)
    userColor.append(color)
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)


def setRandomColor(strip, color, wait_ms=50):
    randomInt = random.randint(1, 60)
    # strip.setPixelColor(randomInt, color)
    # strip.show()
    j = 59
    for i in range(strip.numPixels()):
        if i <= j:
            strip.setPixelColor((j - i), color)
            strip.show()
            time.sleep(wait_ms/1000.0)
    for k in range(strip.numPixels()):
        if k <= j:
            strip.setPixelColor((j - k), userColor[0])
            strip.show()
            time.sleep(wait_ms/1000.0)
    usedColorStrip.update({randomInt: color})
    for keys, values in usedColorStrip.items():
        strip.setPixelColor(keys, values)
        strip.show()


@app.route("/led/<color>/<state>")
def set_led(color, state):
    for webColor in leds.keys():
        if color == webColor:
            if state == 'on':
		    #           GPIO.output(leds[color], 1)
                colorWipe(strip, Color(
                    leds[webColor][0], leds[webColor][1], leds[webColor][2]))  # Red wipe
                print("randome Color?")
                print(userColor)
                return 'LED On: {}'.format(color)
            else:
		    #           GPIO.output(leds[color], 0)
                colorWipe(strip, Color(0, 0, 0))
                print("if randome color click? im here?")
                print(userColor)
                return 'LED Off: {}'.format(color)

        if color == "randomeColor":
            randomG = random.randint(0, 255)
            randomR = random.randint(0, 255)
            randomB = random.randint(0, 255)
            #print(randomColor)
            print("userColor?")
            print(userColor)
            setRandomColor(strip, Color(randomG, randomR, randomB))

            return 'Invalid LED: {}'.format(color)


app.add_url_rule("/", "index", lambda: 'Hello World!')
# Main program logic follows:
if __name__ == '__main__':

    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true',
                        help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(
    	LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    setup()
    app.run(host='0.0.0.0')

    print('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')
