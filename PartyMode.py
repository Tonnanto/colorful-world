import math
import random
import numpy as np
from base_classes import *
from datetime import datetime, timedelta


class PartyMode(Mode):
    key = "PARTY"
    pos = 0  # party pos
    index = 4
    refTime = datetime.now()
    
    center = (19, 14)
    
    randomColors = []
    
    backgroundColor = C.from24bit(0)
    
    def __init__(self, variant, speed):
        self.speed = speed
        self.variant = variant 
        
        for i in range(0, 20):
            PartyMode.randomColors.insert(i, self.randomColor())
        PartyMode.backgroundColor = mapColor(1, 0, 50, C.from24bit(0), self.randomColor())

        clear()
        
    def args(self):
        return str(self.variant)+","+str(self.speed)
    
    def copy(self):
        return PartyMode(self.variant, self.speed)
    
    def loop(self, _leds):
        
        for led in _leds:
            led.c = PartyMode.backgroundColor
        
        if self.variant == 0:
            self.normal( _leds)
            
        elif  self.variant == 1:
            self.chill( _leds)
            
        elif self.variant == 2:
            self.trippy( _leds)
            
        for led in _leds:
            led.load()
        

    # --------------------- NORMAL ----------------------
    def normal(self, _leds):
        refTime = PartyMode.refTime
        currentTime = datetime.now()
        pos = PartyMode.pos
        PartyMode.pos += (currentTime - refTime).total_seconds() * int(self.speed)
        PartyMode.refTime = currentTime
        
        center = PartyMode.center
        
        if (PartyMode.index == 0):
            self.h_line(_leds, self.wheel(125))
            if (pos >= 180):
                PartyMode.refTime = datetime.now()
                PartyMode.pos = 0
                PartyMode.index = 1
            
        elif (PartyMode.index == 1):
            self.v_line(_leds, self.wheel(255))
            if (pos >= 360):
                PartyMode.refTime = datetime.now()
                PartyMode.pos = 0
                PartyMode.index = 2
                
        elif (PartyMode.index == 2):
            self.circle(_leds, False, [(0, self.wheel(0), (center[0], center[1])),
                                        (80, self.wheel(40), (center[0], center[1])),
                                        (160, self.wheel(80), (center[0], center[1])),
                                        (240, self.wheel(150), (center[0], center[1])),
                                        (320, self.wheel(210), (center[0], center[1])),])
            if (pos >= 360):
                PartyMode.refTime = datetime.now()
                PartyMode.pos = 0
                PartyMode.index = 4
                
                
        elif (PartyMode.index == 3):
            ring_1_color = PartyMode.randomColors[5]
            ring_2_color = PartyMode.randomColors[6]
            ring_3_color = PartyMode.randomColors[7]
            ring_4_color = PartyMode.randomColors[8]
            ring_5_color = PartyMode.randomColors[9]
            
            if pos >= 2000:
                ring_1_color = mapColor(pos, 2000, 2200, PartyMode.randomColors[5], PartyMode.backgroundColor)
                ring_2_color = mapColor(pos, 2000, 2200, PartyMode.randomColors[6], PartyMode.backgroundColor)
                ring_3_color = mapColor(pos, 2000, 2200, PartyMode.randomColors[7], PartyMode.backgroundColor)
                ring_4_color = mapColor(pos, 2000, 2200, PartyMode.randomColors[8], PartyMode.backgroundColor)
                ring_5_color = mapColor(pos, 2000, 2200, PartyMode.randomColors[9], PartyMode.backgroundColor)
                
                if pos >= 2200:
                    PartyMode.refTime = datetime.now()
                    PartyMode.pos = 0
                    PartyMode.index = 4

            self.circle(_leds, False, [(0, ring_1_color, (center[0], center[1])),
                                        (72, ring_2_color, (center[0], center[1])),
                                        (144, ring_3_color, (center[0], center[1])),
                                        (216, ring_4_color, (center[0], center[1])),
                                        (288, ring_5_color, (center[0], center[1]))])

                
                
        elif (PartyMode.index == 4):  # 3 Spinning Lines
            line_1_color = PartyMode.randomColors[2]
            line_2_color = PartyMode.randomColors[3]
            line_3_color = PartyMode.randomColors[4]
            
            if pos >= 2000:
                line_1_color = mapColor(pos, 2000, 2200, PartyMode.randomColors[2], PartyMode.backgroundColor)
                line_2_color = mapColor(pos, 2000, 2200, PartyMode.randomColors[3], PartyMode.backgroundColor)
                line_3_color = mapColor(pos, 2000, 2200, PartyMode.randomColors[4], PartyMode.backgroundColor)
                
                if pos >= 2200:
                    PartyMode.refTime = datetime.now()
                    PartyMode.pos = 0
                    PartyMode.index = 3
            
            self.spinningLine(_leds, line_1_color, center = (31, -105), constant = 0, mult = -1.4)
            self.spinningLine(_leds, line_2_color, center = (23, 10), constant = 0, mult = 1.8)
            self.spinningLine(_leds, line_3_color, center = (0, 115), constant = 0, mult = -0.8)
            
            
                
                

    
    # --------------------- CHILL ----------------------
    def chill(self, _leds):
        refTime = PartyMode.refTime
        currentTime = datetime.now()
        pos = PartyMode.pos
        PartyMode.pos += (currentTime - refTime).total_seconds() * int(self.speed)
        PartyMode.refTime = currentTime
        
    
    # --------------------- TRIPPY ----------------------
    def trippy(self, _leds):
        refTime = PartyMode.refTime
        currentTime = datetime.now()
        pos = PartyMode.pos
        PartyMode.pos += (currentTime - refTime).total_seconds() * int(self.speed * 2.4)
        PartyMode.refTime = currentTime
        
        for led in _leds:
            led.c = self.wheelWithColor(int(int(dist(led, 0, 0) * 256 / 180 / 0.4) - pos) & 255, self.wheel(int(pos / 50) & 255))
        
            
            
    def h_line(self, _leds, color):
        lat = 90 - (PartyMode.pos % 180)
        
        for led in _leds:
            offset = lat - led.lat
            if (offset >= -5 and offset <= 5):
                led.c = C.fromRGB(color.r * (255 - abs(offset * 51)) / 255, color.g * (255 - abs(offset * 51)) / 255, color.b * (255 - abs(offset * 51)) / 255)
            else:
                led.c = PartyMode.backgroundColor
                
    def v_line(self, _leds, color):
        long = -180 + (PartyMode.pos % 360)
        
        for led in _leds:
            offset = long - led.long
            if (offset >= -5 and offset <= 5):
                led.c = C.fromRGB(color.r * (255 - abs(offset * 51)) / 255, color.g * (255 - abs(offset * 51)) / 255, color.b * (255 - abs(offset * 51)) / 255)
            else:
                led.c = PartyMode.backgroundColor
                
    def circle(self, _leds, reverse, settings): #settings: [(posOffset, color, center(lat, long))]
                
        for led in _leds:
            #led.c = PartyMode.backgroundColor
            for setting in settings:
                d = (PartyMode.pos + setting[0]) % 360
                if reverse: d = 360 - d
                offset = d - dist(led, setting[2][0], setting[2][1])
                if abs(offset) <= 5:
                    color = setting[1]
                    led.c = mapColor(offset, 0, 5, color, PartyMode.backgroundColor)
                    #led.c = C(color.r * (255 - abs(offset * 51)) / 255, color.g * (255 - abs(offset * 51)) / 255, color.b * (255 - abs(offset * 51)) / 255)
    
    def spinningLine(self, _leds, color, center, constant, mult):
        angle = (mult * (PartyMode.pos * 0.6 + constant)) % 180
        
        for led in _leds:
            
            ledAngle = 90 + math.degrees(math.atan((led.lat-center[0])/(led.long-center[1])))
            
            angleOffset = 440 / dist(led, center[0], center[1])
            angleDifference = abs(ledAngle - angle)
            if angleDifference > 90: angleDifference = 180 - angleDifference
            if angleDifference <= angleOffset:
                led.c = mapColor(angleDifference, 0, angleOffset, color, PartyMode.backgroundColor)
                
                
    def dist(self, point, line): # point(lat, long)  line(p1, p2)
            
        p1 = line[0]
        p2 = line[1]
        p3 = point
             
        d = np.linalg.norm(np.cross(p2-p1, p1-p3))/np.linalg.norm(p2-p1)
        return d

    
    def wheel(self, pos):
        if pos < 85:
            return C.fromRGB(255 - pos * 3, pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return C.fromRGB(0, 255 - pos * 3, pos * 3)
        else:
            pos -= 170
            return C.fromRGB(pos * 3, 0, 255 - pos * 3)
                    
            
    def wheelWithColor(self, pos, color):
        if pos < 85:
            return mapColor(2, 0, 5, C.fromRGB(255 - pos * 3, pos * 3, 0), color)
        elif pos < 170:
            pos -= 85
            return mapColor(2, 0, 5, C.fromRGB(0, 255 - pos * 3, pos * 3), color)
        else:
            pos -= 170
            return mapColor(2, 0, 5, C.fromRGB(pos * 3, 0, 255 - pos * 3), color)
        

    def randomColor(self):
        pos = int(random.random() * 255)
        return self.wheel(pos)
        