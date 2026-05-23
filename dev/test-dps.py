#!/Users/ahmosys/Developer/tools/raycast/raycast-script-cmd/.venv/bin/python3

import os
import time
from dotenv import load_dotenv
from tinytuya import BulbDevice

load_dotenv()

ROOM_LED_STRIP_IP = os.getenv("ROOM_LED_STRIP_IP")
ROOM_LED_STRIP_DEVICE_ID = os.getenv("ROOM_LED_STRIP_DEVICE_ID")
ROOM_LED_STRIP_LOCAL_KEY = os.getenv("ROOM_LED_STRIP_LOCAL_KEY")

print("=== Test des DPS Cachés (22 & 23) ===")

try:
    bulb = BulbDevice(
        dev_id=ROOM_LED_STRIP_DEVICE_ID,
        address=ROOM_LED_STRIP_IP,
        local_key=ROOM_LED_STRIP_LOCAL_KEY,
        version=3.5
    )
    bulb.set_socketPersistent(True)

    print("\n1. Passage en mode 'white'...")
    bulb.set_mode('white')
    time.sleep(1)

    print("\n2. Tentative d'écriture sur DPS 22 (Luminosité) et 23 (Température)...")

    # On essaie d'allumer en Blanc Chaud (Warm)
    # DPS 22: Luminosité (10-1000) -> 1000
    # DPS 23: Température (0-1000) -> 0 (Chaud)

    dps_payload = {
        '22': 1000,
        '23': 0
    }

    print(f"   Envoi: {dps_payload}")
    bulb.set_multiple_values(dps_payload)

    print("\n3. Vérification de l'état...")
    time.sleep(2)
    status = bulb.status()
    print(f"   État actuel: {status}")

    print("\nSi la lumière est allumée en blanc chaud, c'est gagné !")

except Exception as e:
    print(f"Erreur: {e}")
