# Pi Pico MIDI controller

import board
import digitalio
import time
import busio
import adafruit_midi
from adafruit_midi.control_change import ControlChange
from analogio import AnalogIn

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

CHANNEL = 1

uart = busio.UART(board.GP0, board.GP1, baudrate=31250, timeout=0.001)
midi = adafruit_midi.MIDI(midi_out=uart, midi_in=uart, out_channel=CHANNEL - 1, debug=False)

mux_0 = digitalio.DigitalInOut(board.GP18)  # GP18
mux_1 = digitalio.DigitalInOut(board.GP19)  # gp19
mux_2 = digitalio.DigitalInOut(board.GP20)

mux_0.direction = digitalio.Direction.OUTPUT
mux_1.direction = digitalio.Direction.OUTPUT
mux_2.direction = digitalio.Direction.OUTPUT

mux_0.value = True
mux_1.value = True
mux_2.value = True

mux_reading = AnalogIn(board.GP28)
mux_reading.direction = digitalio.Direction.INPUT


while True:
    # read potentiometer
    # set digital pins
    mux_0.value = True
    mux_1.value = True
    mux_2.value = True
    pot_value = mux_reading.value
    print('pot_value: ', pot_value)
    # read/store mux_reading
    # wait?
    # repeat
    # output midi
    # midi.send(ControlChange(30, 20))
    led.value = not led.value
    time.sleep(2)
