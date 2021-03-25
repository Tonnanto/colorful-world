#MQTT Service
import paho.mqtt.client as mqtt


from base_classes import *
from still_mode import *
from rainbow_mode import *
from day_and_night_mode import *
from party_mode import *
from music_mode import *

class MQTTService:
    
    

    def __init__(self):
        self.clientName = "neopixel"
        self.serverAdress = "localhost"
        self.client = mqtt.Client(self.clientName)

        # Topics to subscribe
        self.topics = ["NEO/#"]
        self.cntrlrKey = "CNTRLR"
        
        self.client.on_connect = self.connectionStatus
        self.client.on_message = self.messageDecoder
        self.client.on_log = self.on_log
        
    def connect(self):
        self.client.connect(self.serverAdress)
        
    def loop_start(self):
        self.client.loop_start()
        
    # fires on connect:
    def connectionStatus(self, client, userdata, flags, rc):
        print("connected to MQTT Server")

        for topic in self.topics:
            client.subscribe(topic)
            print("Subscribed to: " + topic)
            
            
    # fires on message:
    def messageDecoder(self, client, userdata, msg):
        
        message = msg.payload.decode(encoding = 'UTF-8')
        topic = msg.topic

        print("message recieved (" + topic + "): " + message)
        
        if "GET_MODES" in topic:
            self.publishModes()
            
            
        elif "SET_MODE" in topic:
            mode = Mode()
            params = message.split(",")
            
            if "STILL" in topic:
                variant = int(params[0])
                mode = StillMode(variant)
            
            if "COLOR" in topic:
                r = int(params[0]); g = int(params[1]); b = int(params[2])
                mode = ColorMode(C.from24bit(0), C.fromRGB(r, g, b))
                
            if "RAINBOW" in topic:
                variant = int(params[0])
                speed = float(params[1])
                _range = float(params[2])
                mode = RainbowMode(variant, speed, _range)
                
            if "DAYANDNIGHT" in topic:
                r = True
                if (params[0] == "false"):
                    r = False
                s = float(params[1])
                mode = DayAndNightMode(r, s)
                
            if "PARTY" in topic:
                variant = int(params[0])
                speed = float(params[1])
                mode = PartyMode(variant, speed)
                
            if "MUSIC" in topic:
                variant = int(params[0])
                shape = int(params[1])
                mode = MusicMode(variant, shape)
                
            if "WORLD" in topic: # set mode fpr all continents
                worlds["WORLD"].setMode(mode)
                worlds["WORLD"].publishMode(self)
                
            else:
                for c in continents.values():
                    if c.name in topic:
                        c.setMode(mode.copy())
                        c.publishMode(self)
                
        elif "GET_BRIGHTNESS" in topic:
            self.publishBrightness()
            
        elif "SET_BRIGHTNESS" in topic:
            val = int(message)
            if val > 255: val = 255
            elif val < 0: val = 0
            
            LED_BRIGHTNESS = val
            strip.setBrightness(val)
            self.publishBrightness()

                    
    # fires on log
    def on_log(self, client, userdata, level, buf):
        print("log: ",buf)
        
    def publishModes(self):
        worlds["WORLD"].publishMode(self)
                                
        for c in continents.values():
            c.publishMode(self)
                
        print("Modes published")
        
    def publishBrightness(self):
        key = self.cntrlrKey+"/RESP_BRIGHTNESS"
        self.client.publish(key, strip.getBrightness())



