# Local LoRa Temperature Probe Sensor

MicroPython client for a Raspberry Pi Pico, an RFM95, and a DS18B20. It reads the probe, converts to Fahrenheit, and sends the reading with RadioHead `send_to_wait` so the bridge can ACK it.

Companion receiver: [Lora to Ethernet Bridge](https://github.com/scottlecomte/Lora-to-Ethernet-Bridge). This node is client address 3 and the bridge is server address 2, on 915 MHz. Change `config.py` if your wiring or addresses differ.

## Hardware

| Item | This tree |
|------|-----------|
| MCU | Raspberry Pi Pico (RP2040), MicroPython |
| Radio | RFM95. CS GP8, reset GP9, DIO0 GP10, SPI0 (`SPIConfig.rp2_0`) |
| Probe | DS18B20 data on GP28 |
| LEDs | GP13 stays on when the board is up. GP12 blinks on each send |

While the temperature is steady, `HEARTBEAT_S` is 300 seconds between readings. While it is moving (more than `TEMP_DELTA_F`, 1.0 Fahrenheit, from the last value sent), readings go out every `FAST_INTERVAL_S` (10 seconds). `ACK_RETRIES` is 2, so three tries total if the bridge does not ACK.

## Layout

```
main.py
config.py
lib/ulora.py
```

Flash `main.py` and `config.py` to the Pico, and put `ulora.py` under `lib/`, with Thonny or `mpremote`.
