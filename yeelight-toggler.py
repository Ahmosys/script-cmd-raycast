#!/usr/bin/env python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Yeelight Toggler
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 💡
# @raycast.packageName Yeelight Toggler

# Documentation:
# @raycast.description Control the state of the Yeelight Bulbs
# @raycast.author ahmosys
# @raycast.authorURL https://raycast.com/ahmosys

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

def toggle_light(bulb: Bulb) -> bool:
    """Toggle the bulb state."""
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

if __name__ == "__main__":
    bulb = get_bulb()
    # Exit if the bulb is not found
    if not bulb:
        sys.exit(1)
    # Toggle the light state
    toggle_light(bulb)
