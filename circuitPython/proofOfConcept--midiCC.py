# Pi Pico MIDI controller


import board
import digitalio
import time
import busio
import adafruit_midi


led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

CHANNEL = 1

uart = busio.UART(board.GP0, board.GP1, baudrate=31250, timeout=0.001)
midi = adafruit_midi.MIDI(midi_out=uart, midi_in=uart, out_channel=CHANNEL, debug=False)


while True:
    led.value = True
    time.sleep(2)
    led.value = False
    time.sleep(1)
# Pi Pico MIDI controller


import board
import digitalio
import time
import busio
import adafruit_midi
from adafruit_midi.control_change import ControlChange


led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

CHANNEL = 1

uart = busio.UART(board.GP0, board.GP1, baudrate=31250, timeout=0.001)
midi = adafruit_midi.MIDI(midi_out=uart, midi_in=uart, out_channel=CHANNEL -1, debug=False)


while True:
    # every 3 seconds, blink LED and change delay time
    midi.send(ControlChange(30, 20))
    led.value = True
    time.sleep(3)
    midi.send(ControlChange(30, 100))
    led.value = False
    time.sleep(3)
