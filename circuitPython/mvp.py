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
SLEEP_TIME = 0.00

uart = busio.UART(board.GP0, board.GP1, baudrate=31250, timeout=0.001)
midi = adafruit_midi.MIDI(midi_out=uart, midi_in=uart, out_channel=CHANNEL - 1, debug=False)

mux_0 = digitalio.DigitalInOut(board.GP18)
mux_1 = digitalio.DigitalInOut(board.GP19)
mux_2 = digitalio.DigitalInOut(board.GP20)

mux_0.direction = digitalio.Direction.OUTPUT
mux_1.direction = digitalio.Direction.OUTPUT
mux_2.direction = digitalio.Direction.OUTPUT

mux_reading = AnalogIn(board.GP28)

button_0 = digitalio.DigitalInOut(board.GP13)
button_1 = digitalio.DigitalInOut(board.GP12)
button_2 = digitalio.DigitalInOut(board.GP11)
button_3 = digitalio.DigitalInOut(board.GP10)

button_0.direction = digitalio.Direction.INPUT
button_1.direction = digitalio.Direction.INPUT
button_2.direction = digitalio.Direction.INPUT
button_3.direction = digitalio.Direction.INPUT

button_0.pull = digitalio.Pull.DOWN
button_1.pull = digitalio.Pull.DOWN
button_2.pull = digitalio.Pull.DOWN
button_3.pull = digitalio.Pull.DOWN

# mapping
midi_cc = [28, 29, 30, 31, 34, 35, 36, 32]
midi_values = [0,0,0,0,0,0,0,0]



# set up
mux_0.value = False
mux_1.value = False
mux_2.value = False

while True:
    # pot 3: 000
    mux_2.value = False
    midi_values[3] = int(mux_reading.value/512) #simpler/faster to bit shift. will try if this is too slow. May be limited by mux chip though.
    time.sleep(SLEEP_TIME)
    # pot 7: 001
    mux_0.value = True
    midi_values[7] = int(mux_reading.value/512)
    time.sleep(SLEEP_TIME)
    # pot 6: 011
    mux_1.value = True
    midi_values[6] = int(mux_reading.value/512)
    time.sleep(SLEEP_TIME)
    # pot 2: 010
    mux_0.value = False
    midi_values[2] = int(mux_reading.value/512)
    time.sleep(SLEEP_TIME)
    # pot 0: 110
    mux_2.value = True
    midi_values[0] = int(mux_reading.value/512)
    time.sleep(SLEEP_TIME)
    # pot 4: 111
    mux_0.value = True
    midi_values[4] = int(mux_reading.value/512)
    time.sleep(SLEEP_TIME)
    # pot 5: 101
    mux_1.value = False
    midi_values[5] = int(mux_reading.value/512)
    time.sleep(SLEEP_TIME)
    # pot 1: 100
    mux_0.value = False
    midi_values[1] = int(mux_reading.value/512)
    time.sleep(SLEEP_TIME)
    #print('midi_values: ', midi_values)
    for i in range(0,8):
        midi.send(ControlChange(midi_cc[i], midi_values[i]))
















