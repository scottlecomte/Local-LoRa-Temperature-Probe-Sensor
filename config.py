# Board wiring and radio settings. Change these to match your build.

# RFM95 / SX1276 pins on the Pico (GP numbers).
RFM95_RST = 9   # radio reset
RFM95_CS = 8    # SPI chip select
RFM95_INT = 10  # DIO0 interrupt

# LoRa channel. Must match the bridge.
RF95_FREQ = 915.0  # MHz
RF95_POW = 20      # transmit power, dBm

# This node and the bridge. Bridge is 2; each sensor needs its own client address.
CLIENT_ADDRESS = 3
SERVER_ADDRESS = 2

# How many extra sends to try if the bridge does not ACK. 2 means three tries total.
ACK_RETRIES = 2

# DS18B20 data pin (GP number).
ONEWIRE_PIN = 28

# Status LEDs (GP numbers). LED stays on when the board is up; LED2 blinks on each send.
LED_PIN = 13
LED_TX_PIN = 12

# Seconds between sends while the coolant temperature is steady.
HEARTBEAT_S = 300  # about 5 minutes; 68-70 F idle is normal

# Seconds between sends while the temperature is moving.
FAST_INTERVAL_S = 10

# Fahrenheit. Farther than this from the last sent value counts as moving.
TEMP_DELTA_F = 1.0

# Repeater. This node stays a client; only the bridge (SERVER_ADDRESS) sends ACKs.
# REPEAT_HOPS is how many rebroadcasts an unstamped packet may still take.
# Each repeater decrements the count in the flags byte (see lib/ulora.py).
REPEAT_ENABLE = True
REPEAT_HOPS = 2
REPEAT_SEEN_MAX = 16
REPEAT_SEEN_MS = 30000
