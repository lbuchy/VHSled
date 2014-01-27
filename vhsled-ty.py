## control script for VHS's wall display array of WS2801 36mm Square LEDs   

import RPi.GPIO as GPIO, time, os, random, requests
import datetime
from vhsled_spi import *
from vhsled_text import *
from vhsled_colour import *
from vhsled_rain import *

GPIO.setmode(GPIO.BCM)

#properties of our display
width = 42
height = 10
strings = ["  PEACE","  LOVE","  VHS!"," WE <3 U","  PLUR","  RAEV","  HEY","  HACK!","VANCOUVER"," SPACE"]

ledpixels = []
for i in range(0,width):
	ledpixels.append([0]*height)

spidev = file("/dev/spidev0.0", "w")        		
random.seed()

## bpm/clock stuff
bpm = 174
interval = float( 250 / bpm )
###interval = ( ( interval / 1000 ) * 4)
interval = 0.125

## enableClock (or not)
enableClock = 1
showClock = enableClock
## enableWords
enableWords = 1

brightness = 0xCC

## Debug
debug = 0

###r = requests.get( 'http://www.random.org/integers/?num=100&min=0&max=2&col=1&base=10&format=plain&rnd=new' )

## LED Clock settings
c = randomColor()
setFullColor(ledpixels,spidev,c)

# a few nice and bright colours with at least one channel at full.
###background_colors = [Color(0,255,0),Color(0,0,255),Color(255,255,0),Color(255,0,255),Color(0,255,255)]
background_colors = [Color(0,0,0),Color(255,0,0),Color(0,255,0),Color(0,0,255)]
text_colors = [Color(0,0,0),Color(255,0,0),Color(0,255,0),Color(0,0,255)]

while (not os.path.exists("/home/pi/stop")):
	action = random.randint(0,2)
	###loopmod = random.randint(2,3)
	loopmod = 2
	if action == 0:
		loopinterval = interval
        elif action == 1:
		loopinterval = interval / loopmod
        elif action == 2:
		loopinterval = interval * loopmod

	if enableClock == 1:
		showClock = random.randint(0,1)

	randomMax = random.randint(0,7)

	colorSwitch = random.randint(0,randomMax)

	if colorSwitch == 0 and showClock == 1:
		if debug:
			print "clock"
        	clockTextOnce(ledpixels,spidev,characters,":",random.choice(background_colors),Color(0,0,0),loopinterval)
	elif colorSwitch == 0 and enableWords == 1:
		if debug:
			print "word"
		displayTextOnce(ledpixels,spidev,characters,random.choice(strings),random.choice(text_colors),random.choice(background_colors),(interval*2))
	elif colorSwitch < randomMax:
		if debug:
			print "flash"
		###colorFlashMode(ledpixels,spidev,random.randint(0,20),loopinterval)
		colorFlashMode(ledpixels,spidev,random.randint(0,1),loopinterval)
	elif colorSwitch == randomMax:
		if debug:
			print "clear"
		setFullColor( ledpixels, spidev, 0 )
		time.sleep( loopinterval )

spidev.close()
if debug:
	print "stopping led display"
