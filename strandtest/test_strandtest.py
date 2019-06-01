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

leds = {
    'red': (0,255,0),
    'blue': (0, 0 ,255),
    'green': (255, 0, 0)
}

userColor = 65280
# print("User Color initialized")
# print(userColor)



# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    userColor = color
    print("here is your user Color")
    print(userColor)
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)


def setRandomColor(strip, color, wait_ms=50):
    randomInt = random.randint(1, 60)
    print("get userColor in Random function")
    print(userColor)
    # strip.setPixelColor(randomInt, color)
    # strip.show()
    j = 59
    for i in range(strip.numPixels()):
        if i <= j:
            strip.setPixelColor((j - i), color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            #strip.setPixelColor((j - i), userColor)
            #strip.show()
            #time.sleep(wait_ms/1000.0)
        #strip.setPixelColor(i, color)
        #strip.show()
    for k in range(strip.numPixels()):
        if k <= j:
            strip.setPixelColor((j - k), userColor)
            strip.show()
            time.sleep(wait_ms/1000.0)
    strip.setPixelColor(randomInt, color)
    strip.show()


@app.route("/led/<color>/<state>")
def set_led(color, state):
    for webColor in leds.keys():   
        if color == webColor:
            if state == 'on':
    #           GPIO.output(leds[color], 1)
                colorWipe(strip, Color(leds[webColor][0], leds[webColor][1], leds[webColor][2]))  # Red wipe
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
            randomColor = (randomG, randomR, randomB)
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
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    app.run(host='0.0.0.0')


    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    # try:

    #     while True:
    #         # print ('Color wipe animations.')
    #         # red = input("Please enter something: ")
            
    #         # blue = input("Please enter something: ")
    #         # green = input("Please enter something: ")
    #         # print("You entered: " + str(red))
    #         # print("You entered: " + blue)
    #         # print("You entered: " + green)
    #         #colorWipe(strip, Color(red, blue, green))
    #         # colorWipe(strip, Color(255, 0, 0))  # Red wipe
    #         # colorWipe(strip, Color(0, 255, 0))  # Blue wipe
    #         # colorWipe(strip, Color(0, 0, 255))  # Green wipe
    #         # colorWipe(strip, Color(0, 255, 123))  # Test wipe
    #         # print ('Theater chase animations.')
    #         # theaterChase(strip, Color(127, 127, 127))  # White theater chase
    #         # theaterChase(strip, Color(127,   0,   0))  # Red theater chase
    #         # theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
    #         # print ('Rainbow animations.')
    #         # rainbow(strip)
    #         # rainbowCycle(strip)
    #         # theaterChaseRainbow(strip)

    # except KeyboardInterrupt:
    #     if args.clear:
    #         colorWipe(strip, Color(0,0,0), 10)
