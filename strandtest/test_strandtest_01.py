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
from socket import *

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

# IP from other Raspberry
SERVER_IP   = "192.168.178.128" 
SERVER_PORT = 50007
CLIENT_PORT = 50008
PORT = 50007
BUFSIZE = 1024

# Button Pin Configuration
ButtonPin = 24
# Set Led status to True(OFF)
Led_status = True


leds = {
    'red': (255, 0, 0),
    'blue': (0, 0, 255),
    'green': (0, 255, 0),
    'cf398e': (207, 57, 142),
    'e43fc8': (228, 63, 200),
    'c8629c' : (200, 98, 156),
    'd94b9c' : (217, 75, 156),
    'c452d9' : (196, 82, 217),
    'be37a3' : (190, 55, 163),
    'b945d5' : (185, 69, 213),
    '8708a8' : (135, 8, 168),
    'a60cb7' : (166, 12, 183),
    '7d2494' : (125, 36, 148),
    '8d1faa' : (141, 31, 170),
    '6a1480' : (106, 20, 128),
    '56016b' : (86, 1, 107),
    'a62ac4' : (166, 42, 196),
    'c162c8' : (193, 98, 200),
    'c862c1' : (200, 98, 193),
    '7d2494' : (125, 36, 148),
    'cc4aec' : (204, 74, 236),
    '9a02bf' : (154, 2, 191),
    '791292' : (121, 18, 146),
    '7a288e' : (122, 40, 142),
    '8105d2' : (129, 5, 210),
    '6f72c5' : (111, 114, 197),
    'af8af1' : (175, 138, 241),
    'b37ddc' : (179, 125, 220),
    'a262c8' : (162, 98, 200),
    'b876cf' : (184, 118, 207),
    'b97ddc' : (185, 125, 220),
    '7d8adc' : (125, 138, 220),
    'a37ddc' : (163, 125, 220),
    '967ddc' : (150, 125, 220),
    '867ddc' : (134, 125, 220),
    '595ef9' : (89, 94, 249),
    '44dcfb' : (68, 220, 251),
    '598ef9' : (89, 142, 249),
    '7d9ddc' : (125, 157, 220),
    '7b72ff' : (123, 114, 255),
    '598ef9' : (89, 142, 249),
    '7d93dc' : (125, 147, 220),
    '18b2ec' : (24, 178, 236),
    '6a82f6' : (106, 130, 246),
    '72a1ff' : (114, 161, 255),
    '3678ff' : (54, 120, 255),
    '7d9ddc' : (125, 157, 220),
    '444aeb' : (68, 74, 235),
    '0414a2' : (4, 20, 162),
    '9bbcff' : (155, 188, 255),
    '021088' : (2, 16, 136),
    '4984fb' : (73, 132, 251),
    '5a91ff' : (90, 145, 255),
    'a2c1ff' : (162, 193, 255),
    'c5d8ff' : (197, 216, 255),
    'e4edff' : (288, 237, 255),
    'd4e3ff' : (212, 227, 255),
    '18ecd0' : (24, 236, 208),
    '18e5ec' : (24, 229, 236),
    '39dbe1' : (57, 219, 225),
    '05d2af' : (5, 210, 175),
    '4481fb' : (68, 129, 251),
    '632971' : (99, 41, 113),
    '048397' : (4, 131, 151),
    '1b599f' : (27, 89, 159),
    '0499b1' : (4, 153, 177),
    '39e166' : (57, 225, 102),
    '3df9ae' : (61, 249, 174),
    '18ec9d' : (24, 236, 157),
    '18ec34' : (24, 236, 52),
    '18ec74' : (24, 236, 116),
    '00c10d' : (0, 193, 13),
    '3ca800' : (60, 168, 0),
    '46c900' : (70, 201, 0),
    '05e523' : (5, 229, 35),
    '009e15' : (0, 158, 21),
    '36ae04' : (54, 174, 4),
    '228a3b' : (34, 138, 59),
    '016819' : (1, 104, 25),
    '268200' : (38, 130, 0),
    '1c5803' : (28, 88, 3),
    '015014' : (1, 80, 20),
    '058a24' : (5, 138, 36),
    '41c937' : (65, 201, 55),
    '5a9f2c' : (90, 159, 44),
    '80b530' : (128, 181, 48),
    '30b542' : (48, 181, 66),
    '27b53a' : (39, 181, 58),
    '5eb130' : (94, 177, 48),
    '90d11f' : (144, 209, 31),
    'a8e152' : (168, 225, 82),
    'c7f28b' : (199, 242, 139),
    'dfffb4' : (223, 255, 180),
    'f5ee44' : (245, 238, 68),
    'b8e57a' : (184, 229, 122),
    'd9fea6' : (217, 254, 166),
    '48c900' : (72, 201, 0),
    '398f0a' : (57, 143, 10),
    '72ff24' : (114, 255, 36),
    '43bc00' : (67, 188, 0),
    '3faf03' : (63, 175, 3),
    '55ef00' : (85,239, 0),
    '3dac00' : (61, 172, 0),
    '4ad101' : (74, 209, 1),
    '42b205' : (66, 178, 5),
    'e4ffbc' : (228, 255, 188),
    'c5fc78' : (197, 252, 120),
    'd7fca3' : (215, 252, 163),
    'f2fce2' : (242, 252, 226),
    'e8ffc8' : (232, 255, 200),
    'ff960c' : (25, 150, 12),
    'ffbe0c' : (255, 190, 12),
    'f0f630' : (240, 246, 48),
    'dfd001' : (223, 208, 1),
    'fe0' : (255, 238, 0),
    'bca760' : (188, 167, 96),
    'e2db16' : (226, 219, 22),
    'ebe201' : (235, 226, 1),
    'c1ba0c' : (193, 186, 12),
    'e2db16' : (226, 219, 22),
    'f6f151' : (246, 241, 81),
    'f5f4da' : (245, 244, 218),
    'fff6a7' : (255, 246, 167),
    'eceab7' : (236, 234, 183),
    'f8f383' : (248, 243, 131),
    'e6e156' : (230, 225, 86),
    'cfc91b' : (207, 201, 27),
    'e2db16' : (226, 219, 22),
    'a8a319' : (168, 163, 25),
    'fff6a7' : (255, 246, 167),
    'fffb8d' : (255, 251, 141),
    'fffdcf' : (255, 253, 207),
    'f3ef88' : (243, 239, 136),
    'f3eb07' : (243, 235, 7),
    'c1ba0c' : (193, 168, 12),
    'e2db16' : (266, 219, 22),
    'aca600' : (172, 166, 0),
    'f5f1a1' : (245, 241, 161),
    'd8d467' : (216, 212, 103),
    'b7b116' : (183, 177, 22),
    'ba5e31' : (186, 94, 49),
    'c9703b' : (201, 112, 59),
    'b96a38' : (185, 106, 56),
    'dd945e' : (221, 148, 94),
    'c9703b' : (201, 112, 59),
    'eca875' : (236, 168, 117),
    'f9ca9d' : (249, 202, 157),
    'de864d' : (222, 134, 77),
    'f6b985' : (246, 185, 133),
    'd67640' : (214, 118, 64),
    'be632e' : (190, 99, 46),
    'c76832' : (199, 104, 50),
    'd06f37' : (208, 111, 55),
    'd06e37' : (208, 110, 55),
    'da7a42' : (218, 122, 66),
    'f1a76c' : (241, 167, 108),
    'f9c08a' : (249, 192, 138),
    'c13215' : (193, 50, 21),
    'ab270c' : (171, 39, 12),
    'cf4747' : (207, 71, 71),
    'cb8779' : (203, 135, 121),
    'f4a868' : (244, 168, 104),
    '881700' : (136, 23, 0),
    'eb9861' : (235, 152, 97),
    'ca6434' : (202, 100, 52),
    'd16939' : (209, 105, 57),
    'd36837' : (211, 104, 55),
    'dd6b3d' : (221, 107, 61),
    'dd6c3b' : (221, 108, 59),
    'f9ba89' : (249, 186, 137),
    'f7ab81' : (247, 171, 129),
    'f99d6b' : (249, 157, 107),
    'ea7947' : (234, 121, 71),
    'fab180' : (250, 177, 128),
    'fcdbb7' : (252, 219, 183),
    'fccfb0' : (252, 207, 176),
    'fcceac' : (252,206,172),
    'b52203' : (181, 34, 3),
    'de3e1d' : (222, 62, 29),
    'd55236' : (213, 82, 54),
    'fc9d8a' : (252, 157, 138),
    'd27b5e' : (210, 123, 94),
    'df5b3f' : (223, 91, 63),
    'e17761' : (225, 119, 97),
    'c16060' : (193, 96, 96),
    'c17878' : (193, 120, 120),
    'f29292' : (242, 146, 146),
    'e96e6e' : (233, 110, 110),
    'd9a1a1' : (217, 161, 161),
    'fb9797' : (251, 151, 151),
    'f1c7be' : (241, 199, 190),
    'dc8a79' : (220, 138, 121),
    'ff7d0c' : (255, 125, 12),
    'ba5d2e' : (186, 93, 46),
    'bc6d3b' : (188, 109, 59),
    'ccc97f' : (204, 201, 127),
    'e2db16' : (226, 219, 22),
    'c5be00' : (197, 190, 0),
    'e2db16' : (226, 219, 22),
    'ccfe87' : (204, 254, 135),
    'dfffb4' : (223, 255, 180),
    '398f0a' : (57, 143, 10),
    '5cff04' : (92, 255, 4),
    '7ea9ff' : (126, 169, 255),
    '74a2ff' : (116, 162, 255),
    '44c9fb' : (68, 201, 251),
    'cae152' : (202, 225, 82),
    '019f0c' : (1, 159, 12),
    '0af661' : (10, 246, 97),
    '27ebbc' : (39, 235, 188),
    '048215' : (4, 130, 21),
    '4dae64' : (77, 174, 100),
    '247304' : (36, 115, 4),
    '7da9dc' : (125, 169, 220),
    '05bdd2' : (5, 189, 210),
    '39cae1' : (57, 202, 225),
    '0a7423' : (10, 116, 35),
    '6505d2' : (101, 5, 210),
    '4957dc' : (73, 87, 220)
}

userColor = [0]

getData = {
    0 : 0,
    1 : 0, 
    2 : 0
}

userColor = {
    0 : 0,
    1 : 0,
    2 : 0
}


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

def responde():
   
    s = socket(AF_INET, SOCK_DGRAM)                              
    s.bind(("", PORT))
    print "UDP-Server gestartet..."
    getData.pop(0)
    getData.pop(1)
    getData.pop(2)

    i = 0
    while 1:
        if i <=2:
            data, (client_ip,client_port) = s.recvfrom(BUFSIZE)      
        
            print "[%s %s]: %s" % (client_ip,client_port, data)
            getData.update({i : int(data)})    
            if i == 2:
                for keys, values in userColor.items():
                    msg_out = str(values)
                    s.sendto(msg_out,(client_ip,client_port))
            
            i = i + 1 
        else:
            break
        #break

    s.close()
    setRandomColor(strip, Color(getData[0], getData[1], getData[2]))

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
        responde()


# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)
    
    #responde()


def setRandomColor(strip, color, wait_ms=50):
    randomInt = random.randint(1, 60)
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
    
    responde()


@app.route("/led/<color>/<state>")
def set_led(color, state):
    for webColor in leds.keys():
        if color == webColor:
            if state == 'on':
		    #           GPIO.output(leds[color], 1)
                colorWipe(strip, Color(
                    leds[webColor][1], leds[webColor][0], leds[webColor][2]))  # Red wipe
                userColor.pop(0)
                userColor.pop(1)
                userColor.pop(2)
                userColor.update({ 0 : leds[webColor][1]})
                userColor.update({ 1 : leds[webColor][0]})
                userColor.update({ 2 : leds[webColor][2]})
                return 'LED On: {}'.format(color)
            else:
		    #           GPIO.output(leds[color], 0)
                colorWipe(strip, Color(0, 0, 0))
                return 'LED Off: {}'.format(color)

        if color == "randomeColor":
            responde()

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
    # server()
    app.run(host='0.0.0.0', port='50007')


    print('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')
