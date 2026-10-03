import time
from ulora import LoRa, ModemConfig, SPIConfig
from machine import Pin
import onewire
import ds18x20
import config #imports the configuration settings for the LoRa module and application variables.

# Temperture Sensor Setup
ow = onewire.OneWire(Pin(config.ONEWIRE_PIN))
ds = ds18x20.DS18X20(ow)
devices = ds.scan()
print('found devices:', devices)

# LED Setup
led = Pin(config.LED_PIN, Pin.OUT)
led2 = Pin(config.LED_TX_PIN, Pin.OUT)

# initialise radio
lora = LoRa(SPIConfig.rp2_0, config.RFM95_INT, config.CLIENT_ADDRESS, config.RFM95_CS,
            reset_pin=config.RFM95_RST, freq=config.RF95_FREQ, tx_power=config.RF95_POW, acks=True)

# Set LED on to indicate Everything is operational
led.high()

# loop and send data
while True:
    ds.convert_temp()
    time.sleep(1)
    for device in devices:
        temperture = round(ds.read_temp(device))
    #added 1 to the last number to calibrate
    fahrenheit_temp = (temperture*9/5)+32
    ok = lora.send_to_wait(str(fahrenheit_temp), config.SERVER_ADDRESS, retries=config.ACK_RETRIES)
    led2.high()
    time.sleep(0.5)
    led2.low()
    print("Temperture: ", str(fahrenheit_temp), " - sent ok:", ok)
    time.sleep(config.SEND_INTERVAL_S)
