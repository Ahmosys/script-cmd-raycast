=== Tuya LED Strip Diagnostic (White CCT) ===

1. Full Device Status:
{
  "dps": {
    "20": true,
    "21": "white",
    "24": "03e8023a0000",
    "26": 0,
    "47": 25,
    "53": 10
  }
}

2. DPS Values:
  DPS 20: True
  DPS 21: white
  DPS 24: 03e8023a0000
  DPS 26: 0
  DPS 47: 25
  DPS 53: 10

3. Device Capabilities (dpset):
  {'switch': '20', 'mode': '21', 'brightness': None, 'colourtemp': None, 'colour': '24', 'scene': None, 'scene_data': None, 'timer': '26', 'music': 28, 'value_min': 10, 'value_max': 1000, 'value_hexformat': 'hsv16'}

4. Bulb Type Detection:
  Bulb Type: B

5. Testing Mode Changes:

  Testing 'white' mode...
    Result: {'protocol': 4, 't': 1763847043, 'data': {'dps': {'21': 'white', '20': True}, 'type': 'query'}, 'dps': {'21': 'white', '20': True}}

  Testing 'colour' mode...
    Result: {'protocol': 4, 't': 1763847043, 'data': {'dps': {'21': 'colour'}}, 'dps': {'21': 'colour'}}

6. Current Status After Mode Tests:
  DPS 20: True
  DPS 21: colour
  DPS 24: 03e8023a0000
  DPS 26: 0
  DPS 47: 25
  DPS 53: 10
