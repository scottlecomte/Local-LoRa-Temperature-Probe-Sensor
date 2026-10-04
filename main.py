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
            reset_pin=config.RFM95_RST, freq=config.RF95_FREQ, tx_power=config.RF95_POW, acks=True,
            repeater=config.REPEAT_ENABLE, repeat_hops=config.REPEAT_HOPS,
            repeat_ack_from=config.SERVER_ADDRESS, repeat_seen_max=config.REPEAT_SEEN_MAX,
            repeat_seen_ms=config.REPEAT_SEEN_MS)

# Set LED on to indicate Everything is operational
led.high()

def idle(seconds):
    # Listen, and send one queued rebroadcast per pass. Never from the RX IRQ.
    try:
        lora.set_mode_rx()
    except Exception:
        pass
    start = time.ticks_ms()
    limit = int(seconds * 1000)
    if limit < 1:
        limit = 1
    while time.ticks_diff(time.ticks_ms(), start) < limit:
        lora.service_repeater()
        time.sleep(0.05)

# loop and send data
# Sample every FAST_INTERVAL_S so a jump is not stuck behind the slow timer.
# fast stays on until a sample is within TEMP_DELTA_F of the last value sent.
last_sent_f = None
last_sent_ms = time.ticks_ms()
fast = False

while True:
    ds.convert_temp()
    idle(1)
    for device in devices:
        temperture = round(ds.read_temp(device))
    #added 1 to the last number to calibrate
    fahrenheit_temp = (temperture*9/5)+32

    send_now = last_sent_f is None
    if not send_now:
        delta_f = abs(fahrenheit_temp - last_sent_f)
        elapsed_ms = time.ticks_diff(time.ticks_ms(), last_sent_ms)
        if delta_f > config.TEMP_DELTA_F:
            # Moving. The jump that enters fast mode sends immediately;
            # later moving samples go out on FAST_INTERVAL_S.
            send_now = (not fast) or elapsed_ms >= int(config.FAST_INTERVAL_S * 1000)
            fast = True
        else:
            # Within TEMP_DELTA_F of the last sent value: back to the slow interval.
            fast = False
            send_now = elapsed_ms >= int(config.HEARTBEAT_S * 1000)

    if send_now:
        ok = lora.send_to_wait(str(fahrenheit_temp), config.SERVER_ADDRESS, retries=config.ACK_RETRIES)
        led2.high()
        idle(0.5)
        led2.low()
        print("Temperture: ", str(fahrenheit_temp), " - sent ok:", ok)
        last_sent_f = fahrenheit_temp
        last_sent_ms = time.ticks_ms()

    idle(config.FAST_INTERVAL_S)
