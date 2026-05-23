#!/Users/ahmosys/Developer/tools/raycast/raycast-script-cmd/.venv/bin/python3

import os
import json
from dotenv import load_dotenv
from tinytuya import BulbDevice

# Load environment variables from .env file
load_dotenv()

ROOM_LED_STRIP_IP = os.getenv("ROOM_LED_STRIP_IP")
ROOM_LED_STRIP_DEVICE_ID = os.getenv("ROOM_LED_STRIP_DEVICE_ID")
ROOM_LED_STRIP_LOCAL_KEY = os.getenv("ROOM_LED_STRIP_LOCAL_KEY")

print("=== Tuya LED Strip Diagnostic ===\n")

try:
    bulb = BulbDevice(
        dev_id=ROOM_LED_STRIP_DEVICE_ID,
        address=ROOM_LED_STRIP_IP,
        local_key=ROOM_LED_STRIP_LOCAL_KEY,
        version=3.5
    )
    bulb.set_socketPersistent(True)

    # Get full status
    print("1. Full Device Status:")
    status = bulb.status()
    print(json.dumps(status, indent=2))

    print("\n2. DPS Values:")
    if 'dps' in status:
        for key, value in status['dps'].items():
            print(f"  DPS {key}: {value}")

    print("\n3. Device Capabilities (dpset):")
    print(f"  {bulb.dpset}")

    print("\n4. Bulb Type Detection:")
    bulb.detect_bulb()
    print(f"  Bulb Type: {bulb.bulb_type if hasattr(bulb, 'bulb_type') else 'Unknown'}")

    print("\n5. Testing Mode Changes:")

    # Test white mode
    print("\n  Testing 'white' mode...")
    try:
        result = bulb.set_mode('white')
        print(f"    Result: {result}")
    except Exception as e:
        print(f"    Error: {e}")

    # Test colour mode
    print("\n  Testing 'colour' mode...")
    try:
        result = bulb.set_mode('colour')
        print(f"    Result: {result}")
    except Exception as e:
        print(f"    Error: {e}")

    print("\n6. Current Status After Mode Tests:")
    status = bulb.status()
    if 'dps' in status:
        for key, value in status['dps'].items():
            print(f"  DPS {key}: {value}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
