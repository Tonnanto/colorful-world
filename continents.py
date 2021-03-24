# continents
import base_classes

class Continent:
    
    def __init__(self, name, index, led_strips):
        self.name = name
        self.index = index
        self.mode = base_classes.Mode()
        self.leds = []
        
        self.addLeds(led_strips)
                
        base_classes.continents[self.name] = self
        
    def addLeds(self, led_strips):
        # Initialize Leds with location
        for s in led_strips:
            count = s[0]; fromlat = s[1]; fromlong = s[2]; tolat = s[3]; tolong = s[4];
            
            if (count == 1): # one Led on strip
                led = base_classes.Led(self, fromlat, fromlong)
                self.leds.append(led)
            else:                   # multiple Leds on strip
                for i in range (0, count):
                    lat = fromlat + (tolat - fromlat) / float(count - 1) * i
                    long = fromlong + (tolong - fromlong) / float(count - 1) * i
                    led = base_classes.Led(self, lat, long)
                    self.leds.append(led)
        
    def loop(self):
        self.mode.loop(self.leds)
        
    # only gets called if mode is adjusted individually for continent
    def setMode(self, mode):
        if (mode.key == self.mode.key): # adjust current mode
            if (self.mode.key == "COLOR"):
                fromColor = self.mode.color
                self.mode = base_classes.ColorMode(fromColor, mode.newColor)
            elif (self.mode.key == "RAINBOW"):
                self.mode.speed = mode.speed
                self.mode.variant = mode.variant
                self.mode.range = mode.range
            elif (self.mode.key == "PARTY"):
                self.mode.variant = mode.variant
                self.mode.speed = mode.speed
            elif (self.mode.key == "DAYANDNIGHT"):
                self.mode.setSpeed(mode.speed)
                self.mode.realTime = mode.realTime
            else:
                self.mode = mode
                
        else: # set new mode
            self.mode = mode
            # if individual modes on continents 
            #if len(set(map(lambda x: x.mode.key, base_classes.continents.values()))) > 1:
            World.same_mode = False
            
    def publishMode(self, mqtt):
        key = mqtt.cntrlrKey+"/"+self.name+"/RESP_MODE/"+self.mode.key
        mqtt.client.publish(key, self.mode.args())
    
        
class World:
    
    same_mode = True
    
    def __init__(self, name, continents):
        self.name = name
        self.continents = continents
        self.mode = base_classes.Mode()
        
        base_classes.worlds[self.name] = self
        
    def loop(self):
        self.mode.loop(base_classes.leds)

    def setMode(self, mode):
        
        if (mode.key == self.mode.key):
            if (self.mode.key == "COLOR"):
                mode = base_classes.ColorMode(self.mode.newColor, mode.newColor)
                
            for c in self.continents.values():
                if (c.mode.key == "RAINBOW"):
                    c.mode.speed = mode.speed
                    c.mode.variant = mode.variant
                    c.mode.range = mode.range
                elif (c.mode.key == "PARTY"):
                    c.mode.speed = mode.speed
                    c.mode.variant = mode.variant
                elif (c.mode.key == "DAYANDNIGHT"):
                    c.mode.setSpeed(mode.speed)
                    c.mode.realTime = mode.realTime
                else:
                    c.mode = mode.copy()
                
        else:
            World.same_mode = True
            for c in self.continents.values():
                if mode.key == "NONE":
                    c.mode = base_classes.Mode()
                else:
                    c.mode = mode.copy()
        
        self.mode = mode

            
    def publishMode(self, mqtt):
        key = mqtt.cntrlrKey+"/"+self.name+"/RESP_MODE/"+self.mode.key
        mqtt.client.publish(key, self.mode.args())
    