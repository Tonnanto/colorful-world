""" This file is a mess and i'm aware of that"""
from neopixel import *
from continents import *
from time import time
from datetime import datetime, timedelta
import math
import numpy as np

 
 
# LED strip configuration:
LED_COUNT      = 443
LED_PIN        = 18
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # 0 - 255
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)

continents = {}
worlds = {}
leds = []




#def init_leds(first, last, fromlat, fromlong, tolat, tolong):
#    for i in range (first, last+1):
#        lat = fromlat + (tolat - fromlat) / float(last - first) * (i - first)
#        long = fromlong + (tolong - fromlong) / float(last - first) * (i - first)
#        leds.append(Led(i, lat, long))
    
def init_allleds(): # initialize leds with loction (lat, long)  *must be in correct order*

    #Eurasia
    
    eurasia = Continent("EURASIA", 3, [
                                    (3, 36.57, 38.81, 30.78, 36.4),
                                    (6, 29.05, 36.23, 16.34, 43.95),
                                    (5, 14.11, 44.35, 22.32, 57.65),
                                    (5, 21.41, 52.09, 30.63, 46.48),
                                    (10, 31.6, 49.46, 26.1, 71.74),
                                    (5, 24.52, 73.99, 10.48, 77.72),
                                    (4, 17.04, 79.57, 23.8, 88.33),
                                    (8, 23.59, 91.96, 11.04, 105.98),
                                    (4, 13.7, 107.55, 20.43, 103.03),
                                    (4, 21.85, 105.89, 25.92, 117.75),
                                    (6, 28.35, 119.32, 38.97, 116.19),
                                    (2, 40.81, 117.59, 41.44, 121.44),
                                    (4, 41.19, 126.49, 51.65, 139.72),
                                    (3, 52.6, 139.01, 54.47, 133.94),
                                    (2, 55.84, 134.53, 59.2, 139.67),
                                    (5, 60.45, 143.25, 63.20, 161.18),
                                    (2, 57.01, 159.05, 53.78, 160.09),
                                    (2, 62.03, 168.29, 63.35, 174.96),
                                    (23, 67.49, 177.64, 72.67, 98.73),
                                    (11, 74.02, 94.35, 65.84, 50.3),
                                    (7, 65.88, 46.93, 69.12, 29.96),
                                    (4, 68.99, 23.32, 61.16, 10.12),
                                    (2, 57.96, 14.73, 62.58, 15.91),
                                    (4, 65.4, 27.98, 55.48, 25.08),
                                    (4, 53.37, 22.53, 53.06, 11.9),
                                    (3, 52.27, 7.71, 48.02, 0.2),
                                    (2, 42.16, -2.55, 40.79, -7.23),
                                    (4, 37.76, -5.74, 44.29, 3.69),
                                    (3, 45.15, 6.16, 46.49, 13.25),
                                    (3, 45.81, 15.71, 41.46, 21.58),
                                    (2, 41.77, 24.22, 42.2, 29.27),
                                    (3, 37.92, 29.56, 38.08, 36.45),
                                    #Great Britain:
                                    (1, 53.47, -7.64, 53.47, -7.64),
                                    (2, 52.78, -0.76, 56.06, -3.88)
                                    ])
    
    
    
    #Greenland
    greenland = Continent("GREENLAND", 5, [
                                        # Iceland:
                                        (1, 64.89, -15.82, 64.89, -15.82),
                                        (1, 64.66, -20.74, 64.66, -20.74),
                                        #
                                        (2, 73.2, -50.46, 76.27, -55.3),
                                        (11, 78.55, -65.33, 81.59, -15.83),
                                        (4, 80.54, -23.57, 73.81, -24.19),
                                        (5, 73.02, -29.66, 63.82, -45.12),
                                        (2, 66.33, -49.93, 71.20, -47.99)
                                        ])
    

    #North America
    n_america = Continent("NORTH_AMERICA", 1, [
                                        (5, 28.29, -101.19, 33.5, -87.83),
                                        (12, 31.0, -84.63, 51.66, -65.29),
                                        (3, 52.68, -60.57, 57.59, -69.46),
                                        (5, 60.21, -73.08, 50.9, -77.58),
                                        (5, 50.39, -81.23, 60.79, -103.28),
                                        (5, 62.51, -103.12, 68.73, -84.59),
                                        (2, 70.18, -79.31, 69.83, -70.95),
                                        (2, 69.1, -68.37, 65.32, -70.85),
                                        (13, 64.82, -103.82, 69.06, -146.58),
                                        (5, 62.65, -157.12, 61.36, -136.73),
                                        (9, 60.41, -132.0, 43.87, -115.43),
                                        (10, 41.53, -120.83, 18.1, -97.72),
                                        (2, 16.27, -90.72, 13.8, -86.19)
                                        ])
    #South America
    s_america = Continent("SOUTH_AMERICA", 4, [
                                        (11, -22.27, -68.49, -50.31, -71.56),
                                        (15, -43.38, -68.36, -10.17, -40.27),
                                        (6, -6.61, -39.42, -1.37, -57.82),
                                        (6, 2.89, -54.86, 8.89, -71.09),
                                        (5, 7.47, -74.02, -4.16, -78.89),
                                        (8, -5.98, -78.86, -20.1, -65.69)
                                        ])

    
    #Africa
    africa = Continent("AFRICA", 0, [
                                (16, 5.71, 11.03, -32.18, 20.61),
                                (9, -31.93, 27.7, -8.56, 38.58),
                                (9, -7.17, 33.69, 8.67, 48.5),
                                (10, 7.6, 42.95, 28.26, 30.36),
                                (6, 26.55, 27.34, 32.83, 8.21),
                                (7, 35.04, 7.22, 27.27, -10.19),
                                (6, 25.84, -11.58, 9.52, -11.78),
                                (6, 7.41, -8.88, 8.73, 9.01),
                                #Madagascar:
                                (4, -15.5, 48.79, -23.69, 46.29)
                                ])
    
    eurasia.addLeds([
                #Japan:
                (1, 33.8, 131.86, 33.8, 131.86),
                (2, 33.73, 135.18, 37.05, 139.71),
                (1, 43.81, 143.01, 43.81, 143.01),
                #Philippines:
                (1, 13.8, 122.65, 13.8, 122.65),
                #Indonesia Middle:
                (1, 0.87, 116.72, 0.87, 116.72),
                (1, -3.44, 120.79, -3.44, 120.79),
                (3, 4.73, 116.14, 0.2, 111.05),
                (1, -2.25, 113.19, -2.25, 113.19),
                #Indonesia West:
                (1, -6.65, 106.94, -6.65, 106.94),
                (3, -5.7, 105.24, 1.13, 100.49),
                (1, 3.9, 97.65, 3.9, 97.65),
                (1, -7.32, 110.9, -7.32, 110.9)
                ])
    
    #Australia
    australia = Continent("AUSTRALIA", 2, [
                                        #Papua Newguinea:
                                        (1, -7.53, 141.27, -7.53, 141.27),
                                        (1, -8.17, 147.12, -8.17, 147.12),
                                        (3, -5.94, 145.24, -2.84, 138.43),
                                        #
                                        (3, -19.64, 140.54, -16.0, 134.94),
                                        (2, -13.53, 133.67, -16.16, 130.39),
                                        (6, -15.96, 126.92, -25.28, 116.07),
                                        (2, -27.53, 116.38, -31.64, 117.61),
                                        (3, -32.77, 119.26, -30.12, 130.17),
                                        (4, -30.68, 133.01, -36.83, 142.21),
                                        (5, -36.25, 147.78, -28.43, 152.26),
                                        (5, -28.06, 150.03, -15.46, 142.41),
                                        #New Zealand:
                                        (1, -35.95, 175.25, -35.95, 175.25),
                                        (1, -40.14, 175.69, -40.14, 175.69),
                                        (2, -41.88, 172.85, -43.37, 171.04),
                                        (1, -46.05, 167.8, -46.05, 167.8)
                                        ])
    
    world = World("WORLD", continents)
    
    

# base functions
def clear():
    for led in leds:
        led.c = C.from24bit(0)
        led.load()
        
            
def dist(led, lat, long):
    return math.sqrt((led.lat - lat)**2 + (led.long - long)**2)

def mapColor(value, fromValue, toValue, fromColor, toColor):
    r = fromColor.r + (toColor.r - fromColor.r) / float(abs(toValue - fromValue)) * (value - fromValue)
    g = fromColor.g + (toColor.g - fromColor.g) / float(abs(toValue - fromValue)) * (value - fromValue)
    b = fromColor.b + (toColor.b - fromColor.b) / float(abs(toValue - fromValue)) * (value - fromValue)
    return C.fromRGB(int(r), int(g), int(b))

    
    
# base classes
class C:
    #def __init__(self, r, g, b):
        
        #self.r = r; self.g = g; self.b = b
        
    def __init__(self, rgb):
        self.r = 0
        self.g = 0
        self.b = 0
        self.rgb = rgb
        
    @classmethod
    def fromRGB(cls, r, g, b):
        if r > 255: r = 255
        elif r < 0: r = 0
        if g > 255: g = 255
        elif g < 0: g = 0
        if b > 255: b = 255
        elif b < 0: b = 0
        
        _r = r << 8
        _g = g << 16
        _b = b
        rgb = np.bitwise_or(np.bitwise_or(_r, _g), _b)
        
        c = cls(rgb)
        c.r = r
        c.g = g
        c.b = b
        return c
    
    @classmethod
    def from24bit(cls, rgb):
        return cls(rgb)
        
    def equals(self, c):
        return (self.rgb == c.rgb)
        
class Led:
    def __init__(self, continent, lat, long):
        self.continent = continent
        self.pos = len(leds)
        self.lat = lat
        self.long = long
        self.dist = dist(self, 0, 25) # distance from map center
        self.recentColor = C.from24bit(0)
        self.c = C.from24bit(0)
        self.b = 255
        leds.append(self)
        
    def load(self):
        #r = float(self.c.r) * (float(self.b) / 255.0)
        #g = float(self.c.g) * (float(self.b) / 255.0)
        #b = float(self.c.b) * (float(self.b) / 255.0)
        #print(self.pos, int(g), int(r), int(b))
        strip._led_data[self.pos] = int(self.c.rgb)# * (float(self.b) / 255.0))
        #strip.setPixelColor(self.pos, Color(int(g), int(r), int(b)))
        
   

class Mode:
    key = "NONE"
    fadeInterval = 0.2
    
    def __init__(self):
        self.refTime = datetime.now()
        self.fading = False

    def loop(self, _leds):
        
        if (datetime.now() - self.refTime).total_seconds() < Mode.fadeInterval:
            if not self.fading:
                self.fading = True
                for led in _leds:
                    led.recentColor = led.c
                    
            for led in _leds:
                led.c = mapColor((datetime.now() - self.refTime).total_seconds(), 0.0, Mode.fadeInterval, led.recentColor, C.from24bit(0))
             
        else:
            for led in _leds:
                led.recentColor = C.from24bit(0)
                led.c = C.from24bit(0)
                
        for led in _leds:
            led.load()
            
    def args(self):
        return ""
    
    def copy(self):
        return Mode()
        
        
class ColorMode(Mode):
    key = "COLOR"
    fadeInterval = 0.2
        
    def __init__(self, fromColor, toColor):
        self.refTime = datetime.now()
        self.color = fromColor
        self.newColor = toColor
    
    def loop(self, _leds):
        color = self.newColor
        
        #print("set " + str(self.color.r) + " " + str(self.newColor.r))
        if not self.color.equals(self.newColor):
            refTime = self.refTime
            currentTime = datetime.now()
            seconds = (currentTime - refTime).total_seconds()
            color = mapColor(seconds, 0, ColorMode.fadeInterval, self.color, self.newColor)
            if seconds >= ColorMode.fadeInterval:
                self.color = self.newColor
        
        for led in _leds:
            led.c = color
            led.load()
            
    def args(self):
        return str(self.newColor.r)+","+str(self.newColor.g)+","+str(self.newColor.b)
    
    def copy(self):
        return ColorMode(self.color, self.newColor)
    
 #   def setColor(self, fromColor, toColor):
        





        