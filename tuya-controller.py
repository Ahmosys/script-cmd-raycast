#!/Users/ahmosys/Developer/tools/raycast/raycast-script-cmd/.venv/bin/python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Tuya Controller
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 💡
# @raycast.packageName Tuya Controller

# Documentation:
# @raycast.description Control the state and color of the Tuya Led Strip
# @raycast.author ahmosys
# @raycast.authorURL https://raycast.com/ahmosys

# Arguments:
# @raycast.argument1 { "type": "dropdown", "placeholder": "Color", "optional": true, "data": [{"title": "Red", "value": "red"}, {"title": "Green", "value": "green"}, {"title": "Blue", "value": "blue"}, {"title": "White", "value": "white"}, {"title": "Warm White", "value": "warm"}, {"title": "Cool White", "value": "cool"}, {"title": "Yellow", "value": "yellow"}, {"title": "Purple", "value": "purple"}, {"title": "Cyan", "value": "cyan"}, {"title": "Orange (Warm CCT)", "value": "orange"}] }
# @raycast.argument2 { "type": "text", "placeholder": "Brightness (1-100)", "optional": true }

import os
import sys
from dotenv import load_dotenv
from tinytuya import BulbDevice

# Load environment variables from .env file
load_dotenv()

ROOM_LED_STRIP_IP = os.getenv("ROOM_LED_STRIP_IP")
ROOM_LED_STRIP_DEVICE_ID = os.getenv("ROOM_LED_STRIP_DEVICE_ID")
ROOM_LED_STRIP_LOCAL_KEY = os.getenv("ROOM_LED_STRIP_LOCAL_KEY")

# Color definitions in RGB format
COLORS = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "white": (255, 255, 255),
    "yellow": (255, 255, 0),
    "purple": (128, 0, 128),
    "cyan": (0, 255, 255),
    "orange": (255, 165, 0)
}

def get_led_strip() -> BulbDevice | None:
    """Instantiate and return a Tuya BulbDevice object."""
    try:
        bulb = BulbDevice(dev_id=ROOM_LED_STRIP_DEVICE_ID, address=ROOM_LED_STRIP_IP, local_key=ROOM_LED_STRIP_LOCAL_KEY, version=3.5)
        bulb.set_socketPersistent(True)
        return bulb
    except Exception as e:
        print(f"Error when connecting to led strip: {e}")
        return None

def toggle_light_if_no_arguments(bulb: BulbDevice, color: str, brightness: int) -> bool:
    """Toggle the bulb state only if no color or brightness is specified."""
    if not color and brightness == 100:
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
    else:
        try:
            return bulb.state()["is_on"]
        except Exception as e:
            print(f"Error when checking led strip state: {e}")
            return False

# CCT (Color Temperature) definitions for warm/cool whites
# Format: (brightness_percentage, color_temp)
# color_temp: 0 = Warmest (2700K), 1000 = Coolest (6500K)
# Using safer ranges (10-1000) to avoid potential invalid 0 value
CCT_COLORS = {
    "white": (100, 570),      # Neutral white (Value from working log)
    "warm": (100, 10),        # Warm white (Avoid 0)
    "cool": (100, 990),       # Cool white
    "orange": (100, 10),      # Warmest possible white (Avoid 0)
}

def set_light_color_and_brightness(bulb: BulbDevice, color: str, brightness: int):
    """Set the led strip color and brightness using hybrid mode (Native CCT + RGB)."""
    try:
        brightness = max(1, min(100, int(brightness)))

        # Turn on the strip if it's off
        if not bulb.state()["is_on"]:
            bulb.turn_on()

        if color in CCT_COLORS:
            # --- NATIVE CCT MODE (Using Standard DPS 22/23) ---
            # Schema confirms:
            # bright_value (DPS 22): 10-1000
            # temp_value (DPS 23): 0-1000

            _, target_temp = CCT_COLORS[color]

            # Scale brightness to 10-1000
            val_brightness = int(max(10, brightness * 10))

            # Prepare DPS payload
            # We send Mode + Brightness + Temp together
            dps_data = {
                '21': 'white',      # Mode White
                '22': val_brightness, # Brightness
                '23': target_temp     # Color Temp
            }

            bulb.set_multiple_values(dps_data)

            print(f"Set CCT Mode: {color} (Lum: {val_brightness}, Temp: {target_temp}) -> DPS: {dps_data}")

        elif color in COLORS:
            # --- STANDARD RGB MODE ---
            r, g, b = COLORS[color]

            # Switch to colour mode first
            bulb.set_mode('colour')

            # Then set color and brightness
            bulb.set_colour(r, g, b)
            bulb.set_brightness(brightness)

            print(f"Set RGB Mode: {color} with brightness {brightness}.")
        else:
            print(f"Invalid color specified: {color}")
    except Exception as e:
        print(f"Error when setting the led strip color or brightness: {e}")

def parse_arguments() -> tuple[str, int]:
    """Parse and validate command-line arguments."""
    choice = sys.argv[1].lower() if len(sys.argv) > 1 and sys.argv[1] else ""
    brightness_choice = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 100
    return choice, brightness_choice

if __name__ == "__main__":
    # Validate environment variables
    if not all([ROOM_LED_STRIP_IP, ROOM_LED_STRIP_DEVICE_ID, ROOM_LED_STRIP_LOCAL_KEY]):
        print("Error: Missing required environment variables. Please check your .env file.")
        sys.exit(1)

    bulb = get_led_strip()
    # Exit if the bulb is not found
    if not bulb:
        sys.exit(1)

    # Parse the command-line arguments
    color_choice, brightness_choice = parse_arguments()

    # Toggle the light if no arguments are provided
    is_light_on = toggle_light_if_no_arguments(bulb, color_choice, brightness_choice)

    # If arguments are provided, set the color and brightness
    if is_light_on and color_choice:
        set_light_color_and_brightness(bulb, color_choice, brightness_choice)
    elif color_choice:
        # If color is specified but light is off, turn it on first
        bulb.turn_on()
        set_light_color_and_brightness(bulb, color_choice, brightness_choice)
