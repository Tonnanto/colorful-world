#NeoPixel World
from neopixel import *
from time import (sleep, time)
from datetime import datetime
import RPi.GPIO as GPIO
import argparse

#Custom Classes
from mqtt_service import *
from base_classes import *
from continents import *
from day_and_night_mode import *
from rainbow_mode import *
from music_mode import *


init_allleds()
mqttClient = MQTTService()



#Global Variables
#mode = MusicMode(2, 0)
mode = DayAndNightMode(True, 1)
worlds["WORLD"].setMode(mode)

# ----------------MAIN-------------------
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear LEDs on exit')
    args = parser.parse_args()
    
    
    mqttClient.connect()
    sleep(2)
    mqttClient.loop_start()

    strip.begin()
    mqttClient.publishModes()
    mqttClient.publishBrightness()
    
    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:
        
        mic_check_interval = 2 # s
        mic_check_tmstmp = 0
        
        while True:
            
            if stream_active():
            #    mic_tm = time()##
                microphone_update()
            #    print('microphone_update():', time() - mic_tm)##
                
            # loop modes
            #loop_tm = time()##
            if World.same_mode: # same mode on all continents
                worlds["WORLD"].loop()
            else: # indivudual modes
                for continent in continents.values():
                    continent.loop()
            #print('modes.loop():', time() - loop_tm)##
            
            # load LED color values
            #led_tm = time()##
            #for led in leds:
            #    led.load()
            #print('leds.load():', time() - led_tm)##
            
            #show_tm = time()##
            #sleep(0.001)
            strip.show()
            #print('strip.show():', time() - show_tm)##

            
            # stop microphone stream if no MusicMode active
            if stream_active() and time() > mic_check_tmstmp + mic_check_interval:
                if not 'MUSIC' in set(map(lambda x: x.mode.key, continents.values())):
                    stop_microphone_stream()
                    
                mic_check_tmstmp = time()
                

    except KeyboardInterrupt:
        if args.clear:
            clear()
            strip.show()
