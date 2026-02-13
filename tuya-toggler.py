#!/usr/bin/env python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Tuya Toggler
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 💡
# @raycast.packageName Tuya Toggler

# Documentation:
# @raycast.description Control the state of the Tuya Led Strip
# @raycast.author ahmosys
# @raycast.authorURL https://raycast.com/ahmosys

import os
import sys
from dotenv import load_dotenv
from tinytuya import BulbDevice

# Load environment variables from .env file
load_dotenv()

ROOM_LED_STRIP_IP = os.getenv("ROOM_LED_STRIP_IP")
ROOM_LED_STRIP_DEVICE_ID = os.getenv("ROOM_LED_STRIP_DEVICE_ID")
ROOM_LED_STRIP_LOCAL_KEY = os.getenv("ROOM_LED_STRIP_LOCAL_KEY")

def get_led_strip() -> BulbDevice | None:
    """Instantiate and return a Tuya BulbDevice object."""
    try:
        bulb = BulbDevice(dev_id=ROOM_LED_STRIP_DEVICE_ID, address=ROOM_LED_STRIP_IP, local_key=ROOM_LED_STRIP_LOCAL_KEY, version=3.5)
        bulb.set_socketPersistent(True)
        return bulb
    except Exception as e:
        print(f"Error when connecting to led strip: {e}")
        return None

def toggle_light(bulb: BulbDevice) -> bool:
    """Toggle the bulb state."""
    try:
        current_state = bulb.state()["is_on"]
        if current_state == True:
            bulb.turn_off()
            print("The led strip is now off.")
            return False
        else:
            bulb.turn_on()
            print("The led strip is now on.")
            return True
    except Exception as e:
        print(f"Error when toggling the led strip: {e}")
        return False

if __name__ == "__main__":
    # Validate environment variables
    if not all([ROOM_LED_STRIP_IP, ROOM_LED_STRIP_DEVICE_ID, ROOM_LED_STRIP_LOCAL_KEY]):
        print("Error: Missing required environment variables. Please check your .env file.")
        sys.exit(1)

    bulb = get_led_strip()
    # Exit if the bulb is not found
    if not bulb:
        sys.exit(1)
    # Toggle the light state
    toggle_light(bulb)
