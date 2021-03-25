from base_classes import *
import math
from time import time
from datetime import datetime, timedelta

class DayAndNightMode(Mode):
    key = "DAYANDNIGHT"
    day_color = C.fromRGB(255, 180, 90)
    night_color = C.fromRGB(0, 0, 5)
    set_color = C.fromRGB(255, 80, 0)
    
    tz = 1 
    time = datetime.now()
    refTime = datetime.now()
    speed = 3600
    
    def __init__(self, realTime, speed):
        self.realTime = realTime
        self.setSpeed(speed)
        
    def args(self):
        if (self.realTime):
            return "true,"+str(self.speed)
        else:
            return "false,"+str(self.speed)
        
    def copy(self):
        return DayAndNightMode(self.realTime, DayAndNightMode.speed)
        
    def setSpeed(self, speed):
        DayAndNightMode.refTime = datetime.now()
        DayAndNightMode.speed = speed

    def loop(self, _leds):
        
        #angle = self.calcSunAngle(Led(0, 53.714, 10.218), datetime.now())
        #color = self.colorForAngle(angle)
        #print(angle)
        
        if self.realTime:
            DayAndNightMode.time = datetime.now()
        else:
            refTime = DayAndNightMode.refTime
            currentTime = datetime.now()
                
            DayAndNightMode.time += timedelta(seconds=((currentTime - refTime).total_seconds() * int(self.speed)))
            DayAndNightMode.refTime = currentTime
        
        for led in _leds:
            angle = self.calcSunAngle(led, DayAndNightMode.time)
            color = self.colorForAngle(angle)
            led.c = color
            led.load()
        
        
        #print(self.time)
            
            
    def calcSunAngle(self, led, time):
        N = time.timetuple().tm_yday #
        o = math.degrees(math.asin(0.39795*math.cos(math.radians(0.98563*(N-173)))))#
        LSTM = 15.0 * self.tz
        B = (360.0 / 365.0) * (N - 81.0) #
        EoT = 9.87 * math.sin(math.radians(2 * B)) - 7.53 * math.cos(math.radians(B)) - 1.5 * math.sin(math.radians(B)) #
        TC = 4.0 * (led.long - LSTM) + EoT
        LT = float(time.hour) + (float(time.minute) / 60.0)
        LST = LT + (TC / 60.0)
        HRA = 15.0 * (LST - 12.0)
        preEA1 = math.cos(math.radians(o)) * math.cos(math.radians(led.lat)) * math.cos(math.radians(HRA))
        preEA2 = math.sin(math.radians(o)) * math.sin(math.radians(led.lat))
        EA = math.degrees(math.asin(preEA2 + preEA1))
        return EA
    
    def colorForAngle(self, angle):
        dayangle = 20
        setangle = 5
        nightangle = -10
        if angle > dayangle: return self.day_color
        if angle < nightangle: return self.night_color
        if angle > setangle: # from set to day
            return mapColor(angle, setangle, dayangle, self.set_color, self.day_color)            
            
        if angle <= setangle: # from night to set
            return mapColor(angle, nightangle, setangle, self.night_color, self.set_color)
            