#!/usr/bin/env python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Yeelight Controller
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 💡
# @raycast.packageName Yeelight Controller

# Documentation:
# @raycast.description Control the state of the Yeelight Bulbs
# @raycast.author ahmosys
# @raycast.authorURL https://raycast.com/ahmosys

# Arguments:
# @raycast.argument1 { "type": "dropdown", "placeholder": "Choose a color", "optional": true, "data": [{"title": "White", "value": "white"}, {"title": "Red", "value": "red"}] }

from yeelight import Bulb, BulbException
import sys

ROOM_BULB_IP = "192.168.1.67"

def toggle_light():
    try:
        bulb = Bulb(ROOM_BULB_IP)
        current_state = bulb.get_properties()["power"]
        
        if current_state == "on":
            bulb.turn_off()
            print("The bulb is now off.")
            return False
        else:
            bulb.turn_on()
            print("The bulb is now on.")
            return True 
    except BulbException as e:
        print(f"Error when connecting to bulb: {e}")
        return False

def set_light_color(color):
    try:
        bulb = Bulb(ROOM_BULB_IP)
        if color == "white":
            bulb.set_rgb(255, 255, 255)
            bulb.set_color_temp(4000)
            bulb.set_brightness(100)
            print("The bulb is now white.")
        elif color == "red":
            bulb.set_rgb(255, 0, 0)
            bulb.set_brightness(20)
            print("The bulb is now red.")
        else:
            pass
    except BulbException as e:
        print(f"Error when connecting to bulb: {e}")

if __name__ == "__main__":
    # Toggle the light
    is_light_on = toggle_light()
    # If the light is on and a color is provided, set the color
    if is_light_on and len(sys.argv) > 1:
        color_choice = sys.argv[1].lower()
        set_light_color(color_choice)
