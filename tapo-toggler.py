#!/usr/bin/env python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Tapo Toggler
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 🔌
# @raycast.packageName Tapo Toggler

# Documentation:
# @raycast.description Control the state of the Tapo P110 Smart Plug
# @raycast.author ahmosys
# @raycast.authorURL https://raycast.com/ahmosys

import os
import asyncio

from tapo import ApiClient
from dotenv import load_dotenv

load_dotenv()

TAPO_EMAIL = os.getenv("TAPO_EMAIL")
TAPO_PASSWORD = os.getenv("TAPO_PASSWORD")
TAPO_IP_ADDRESS = os.getenv("TAPO_DEVICE_IP")

async def toggle_plug():
    client = ApiClient(TAPO_EMAIL, TAPO_PASSWORD)
    device = await client.p110(TAPO_IP_ADDRESS)
    try:
        device_info = await device.get_device_info()
        current_state = device_info.device_on
        if current_state == True:
            await device.off()
            print("The plug is now off.")
        else:
            await device.on()
            print("The plug is now on.")
    except Exception as e:
        print(f"Error when toggling the plug strip: {e}")
        return False
    
if __name__ == "__main__":
    asyncio.run(toggle_plug())