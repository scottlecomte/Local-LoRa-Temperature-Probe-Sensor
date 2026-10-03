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

# Seconds to wait between readings.
SEND_INTERVAL_S = 10
