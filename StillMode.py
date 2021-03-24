from base_classes import *

class StillMode(Mode):
    key = "STILL"
    
    def __init__(self, variant):
        self.variant = variant

    def args(self):
        return str(self.variant)
    
    def copy(self):
        return StillMode(self.variant)
    
    def loop(self, _leds):
        
        for led in _leds:
            if self.variant == 0: # Nature
                ice = C.fromRGB(255, 255, 255)
                desert = C.fromRGB(255, 120, 60)
                red_desert = C.fromRGB(255, 82, 0)
                light_forest = C.fromRGB(70, 255, 0)
                dark_forest = C.fromRGB(0, 75, 0)
                rain_forest = C.fromRGB(44, 128, 0)
                coral = C.fromRGB(50, 255, 60)
                
                if led.continent.name == "GREENLAND":
                    led.c = ice
                    
                elif led.continent.name == "AFRICA":
                    if led.lat >= 14:
                        led.c = desert
                    elif led.lat < 14 and led.lat >= -4:
                        led.c = mapColor(led.lat, -4, 14, light_forest, desert)
                    else:
                        led.c = light_forest
                        
                elif led.continent.name == "AUSTRALIA":
                    if led.long > 160: # New Zealand
                        led.c = light_forest
                    elif led.lat >= -10: # Papua New Guinea
                        led.c = coral
                    else:
                        led.c = red_desert
                        
                elif led.continent.name == "EURASIA":
                    if led.lat >= 69:
                        led.c = ice
                    elif led.lat >= 48:
                        led.c = dark_forest
                        
                elif led.continent.name == "NORTH_AMERICA":
                    if led.lat >= 68 or led.long <= -140:
                        led.c = ice
                    elif led.lat >= 43:
                        led.c = dark_forest
                    elif led.lat <= 22 and led.long >= -98:
                        led.c = coral
                        
                #elif led.contnent.name == "SOUTH_AMERICA":
                    
                        
            elif self.variant == 1: # Climate Zones
                polar = C.fromRGB(140, 255, 255)
                subpolar = C.fromRGB(28, 83, 255)
                temperate = C.fromRGB(0, 80, 0)
                subtropical = C.fromRGB(84, 255, 0)
                tropical = C.fromRGB(255, 245, 0)
                subequatorial = C.fromRGB(255, 77, 0)
                equatorial = C.fromRGB(255, 0, 0)
                
                if led.continent.name == "NORTH_AMERICA":
                    if led.lat >= 74: led.c = polar
                        
                    elif led.long <= -99: # West Half
                        if led.lat >= 61: led.c = subpolar
                        elif led.lat >= 47: led.c = temperate
                        elif led.lat >= 33: led.c = subtropical
                        else: led.c = tropical
                        
                    else: # East Half
                        if led.lat >= 52: led.c = subpolar
                        elif led.lat >= 41: led.c = temperate
                        elif led.lat >= 28: led.c = subtropical
                        else: led.c = tropical
                        
                elif led.continent.name == "SOUTH_AMERICA":
                    if led.lat <= -44: led.c = temperate
                    elif led.lat <= -31: led.c = subtropical
                        
                    elif led.long <= -64: # West Half
                        if led.lat >= 2: led.c = subequatorial
                        elif led.lat >= -9: led.c = equatorial
                        elif led.lat >= -19: led.c = subequatorial
                        else: led.c = tropical
                        
                    else: # East Half
                        if led.lat >= 5: led.c = subequatorial
                        elif led.lat >= -4: led.c = equatorial
                        elif led.lat >= -9: led.c = subequatorial
                        else: led.c = tropical
                        
                elif led.continent.name == "GREENLAND":
                    if led.lat >= 66: led.c = polar
                    else: led.c = subpolar
                    
                elif led.continent.name == "EURASIA":
                    if led.lat >= 73: led.c = polar
                        
                    elif led.long <= 65: # West Half
                        if led.lat >= 66: led.c = subpolar
                        elif led.lat >= 43: led.c = temperate
                        elif led.lat >= 33: led.c = subtropical
                        else: led.c = tropical
                        
                    else: # East Half
                        if led.lat >= 60: led.c = subpolar
                        elif led.lat >= 39: led.c = temperate
                        elif led.lat >= 31: led.c = subtropical
                        elif led.lat >= 25: led.c = tropical
                        elif led.lat >= 8: led.c = subequatorial
                        elif led.lat >= -6: led.c = equatorial
                        else: led.c = subequatorial
                        
                elif led.continent.name == "AFRICA":
                    if led.lat >= 33 or led.lat <= -30: led.c = subtropical
                    
                    elif led.long <= 20: # West Half
                        if led.lat >= 19: led.c = tropical
                        elif led.lat >= 8: led.c = subequatorial
                        elif led.lat >= -4: led.c = equatorial
                        elif led.lat >= -12: led.c = subequatorial
                        else: led.c = tropical
                        
                    else: # East Half
                        if led.lat >= 14: led.c = tropical
                        elif led.lat >= 4: led.c = subequatorial
                        elif led.lat >= -8: led.c = equatorial
                        elif led.lat >= -18: led.c = subequatorial
                        else: led.c = tropical
                        
                elif led.continent.name == "AUSTRALIA":
                    if led.lat >= -7: led.c = equatorial
                    elif led.lat >= -19: led.c = subequatorial
                    elif led.lat >= -31: led.c = tropical
                    elif led.lat >= -41: led.c = subtropical
                    else: led.c = temperate
                    
            led.load()
                    
            
                

            
