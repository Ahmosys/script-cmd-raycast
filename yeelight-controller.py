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

def get_bulb() -> Bulb | None:
    """Instantiate and return a Yeelight Bulb object."""
    try:
        return Bulb(ROOM_BULB_IP)
    except BulbException as e:
        print(f"Error when connecting to bulb: {e}")
        return None

def toggle_light_if_no_arguments(bulb: Bulb, color: str, brightness: int) -> bool:
    """Toggle the bulb state only if no color or brightness is specified."""
    if not color and brightness == 100:
        try:
            current_state = bulb.get_properties().get("power")
            if current_state == "on":
                bulb.turn_off()
                print("The bulb is now off.")
                return False
            else:
                bulb.turn_on()
                print("The bulb is now on.")
                return True
        except BulbException as e:
            print(f"Error when toggling the bulb: {e}")
            return False
    else:
        return bulb.get_properties().get("power") == "on"

def set_light_color_and_brightness(bulb: Bulb, color: str, brightness: int) -> None:
    """Set the bulb color and brightness."""
    try:
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
        print(f"Error when setting the bulb color or brightness: {e}")

def parse_arguments() -> tuple:
    """Parse and validate command-line arguments."""
    color_choice = sys.argv[1].lower() if len(sys.argv) > 1 and sys.argv[1] else ""
    brightness_choice = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 100
    return color_choice, brightness_choice

if __name__ == "__main__":
    bulb = get_bulb()
    # Exit if the bulb is not found
    if not bulb:
        sys.exit(1)
    # If no arguments are provided, toggle the light state
    color_choice, brightness_choice = parse_arguments()
    is_light_on = toggle_light_if_no_arguments(bulb, color_choice, brightness_choice)
    # If arguments are provided, set the color and brightness
    if is_light_on and color_choice:
        set_light_color_and_brightness(bulb, color_choice, brightness_choice)
