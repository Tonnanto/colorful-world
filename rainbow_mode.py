# Rainbow Mode
from base_classes import *
from datetime import datetime, timedelta
import time

class RainbowMode(Mode):
    key = "RAINBOW"
    pos = 0.0
    refTime = datetime.now()

    def __init__(self, variant, speed, _range):
        self.speed = speed
        self.range = _range
        self.variant = variant
        
    def args(self):
        return str(self.variant) + "," + str(self.speed) + "," + str(self.range)
    
    def copy(self):
        return RainbowMode(self.variant, self.speed, self.range)
    
    def loop(self, _leds):
        refTime = RainbowMode.refTime
        currentTime = datetime.now()
        pos = RainbowMode.pos
        RainbowMode.pos += float((currentTime - refTime).total_seconds() * (self.speed / ((1 + self.range) / 2)))
        RainbowMode.refTime = currentTime
        
        for led in _leds:
            
            if self.variant == 0:
                led.c = self.wheel(int(pos / self.range) & 255)
              
            elif self.variant == 1:
                led.c = self.wheel(int(int(led.continent.index * 256 / len(continents) / self.range) + pos) & 255)
                
            elif self.variant == 2:
                led.c = self.wheel(int(int(led.pos * 256 / len(_leds) / self.range) + pos) & 255)
                
            elif self.variant == 3:
                led.c = self.wheel(int(int(led.long * 256 / 360 / self.range) + pos) & 255)
                
            elif self.variant == 4:
                led.c = self.wheel(int(int(led.lat * 256 / 180 / self.range) + pos) & 255)
                
            elif self.variant == 5:
                led.c = self.wheel(int(int(dist(led, 0, 0) * 256 / 180 / self.range) - pos) & 255)
                
            led.load()
            

    #def transition(self, variant):
    #    if variant == 0:
            

    def wheel(self, pos):
        if pos < 85:
            return C.fromRGB(255 - pos * 3, pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return C.fromRGB(0, 255 - pos * 3, pos * 3)
        else:
            pos -= 170
            return C.fromRGB(pos * 3, 0, 255 - pos * 3)
        
