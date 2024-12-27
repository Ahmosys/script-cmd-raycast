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
# @raycast.argument1 { "type": "dropdown", "placeholder": "Color", "optional": true, "data": [{"title": "White", "value": "white"}, {"title": "Red", "value": "red"}, {"title": "Cozy", "value": "cozy"}] }
# @raycast.argument2 { "type": "text", "placeholder": "Brightness (1-100)", "optional": true }

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

def set_light_color_and_brightness(color, brightness):
    try:
        bulb = Bulb(ROOM_BULB_IP)
        brightness = max(1, min(100, int(brightness)))
        
        if color == "white":
            bulb.set_color_temp(4000)
            bulb.set_brightness(brightness)
            print(f"The bulb is now white with brightness {brightness}.")
        elif color == "red":
            bulb.set_rgb(255, 0, 0)
            bulb.set_brightness(brightness)
            print(f"The bulb is now red with brightness {brightness}.")
        elif color == "cozy":
            bulb.set_color_temp(2700)
            bulb.set_brightness(brightness)
            print(f"The bulb is now cozy with brightness {brightness}.")
        else:
            print("Invalid color specified.")
    except BulbException as e:
        print(f"Error when connecting to bulb: {e}")

if __name__ == "__main__":
    # Toggle the light
    is_light_on = toggle_light()
    color_choice = sys.argv[1].lower() if len(sys.argv) > 1 and sys.argv[1] else ""
    brightness_choice = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 100

    # If the light is on and arguments are provided, set the color and brightness
    if is_light_on and color_choice and brightness_choice:
        set_light_color_and_brightness(color_choice, brightness_choice)
