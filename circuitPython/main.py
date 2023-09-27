# Pi Pico MIDI controller
import adafruit_midi
import board
import busio
import digitalio
import time

from adafruit_midi.control_change import ControlChange
from analogio import AnalogIn

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

CHANNEL = 1

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
# MIDI CCs
# Mod Time: 28
# Mod Depth: 29
# Delay Time: 30
# Delay Depth: 31
# Reverb Time: 34
# Reverb Depth: 35
# Reverb Mix: 36

midi_cc = [28, 29, 30, 31, 34, 35, 36]
new_midi_values = [0,0,0,0,0,0,0]
current_midi_values = [0,0,0,0,0,0,0]

pot_readings = [0,0,0,0,0,0,0,0]


mux_0.value = False
mux_1.value = False
mux_2.value = False

lfo_last_update = time.monotonic()
lfo_step = -1
lfo_range = 15
lfo_value = 0
lfo_output = 0
lfo_destination = [0,0,0,0,0,1,0] #default to Reverb Depth


while True:
    ## Read Potentiometers (Gray Codes for speed and accuracy)##
    # pot 3: 000
    mux_2.value = False
    pot_readings[3] = mux_reading.value >> 9
    # pot 7: 001
    mux_0.value = True
    pot_readings[7] = mux_reading.value >> 9
    # pot 6: 011
    mux_1.value = True
    pot_readings[6] = mux_reading.value >> 9
    # pot 2: 010
    mux_0.value = False
    pot_readings[2] = mux_reading.value >> 9
    # pot 0: 110
    mux_2.value = True
    pot_readings[0] = mux_reading.value >> 9
    # pot 4: 111
    mux_0.value = True
    pot_readings[4] = mux_reading.value >> 9
    # pot 5: 101
    mux_1.value = False
    pot_readings[5] = mux_reading.value >> 9
    # pot 1: 100
    mux_0.value = False
    pot_readings[1] = mux_reading.value >> 9

    ## Map Potentiometer Readings to Midi CCs ##
    new_midi_values[0] = pot_readings[0]    # Pot 0: Mod Time
    new_midi_values[1] = pot_readings[1]    # Pot 1: Mod Depth
    new_midi_values[2] = pot_readings[2]    # Pot 2: Delay Time
    new_midi_values[3] = pot_readings[3]    # Pot 3: Delay Depth
    new_midi_values[4] = pot_readings[4]    # Pot 4: Reverb Time
    new_midi_values[5] = pot_readings[5]    # Pot 5: Reverb Depth
    new_midi_values[6] = pot_readings[6]    # Pot 6: Reverb Mix


    ## Read Buttons and Map to LFO Outputs

    if button_0.value:
        lfo_destination = [1,0,0,0,0,0,0] #mod time
        print('mod time')
    if button_1.value:
        lfo_destination = [0,0,1,0,0,0,0] #delay time
        print('delay time')
    if button_2.value:
        lfo_destination = [0,0,0,1,0,0,0] #delay depth
        print('delay depth')
    if button_3.value:
        lfo_destination = [0,0,0,0,0,1,0] #reverb depth
        print('verb depth')

    ## Do the Low Frequency Oscillation
    if pot_readings[7] == 0:
        lfo_value = 0
    else:
        # Translate pot 7 to a time interval and to LFO Range
        lfo_update_interval = 0.001 + 0.005*pot_readings[7]/8  # minimum 0.01 seconds between change plus 0 to 128*2*10 milliseconds
        lfo_range = pot_readings[7] >> 2  # allow 0-25% up or down

        # Is it time yet?
        if time.monotonic() >= (lfo_last_update + lfo_update_interval):
            lfo_last_update = time.monotonic()
            lfo_value += lfo_step

            # If lfo_value is bigger or smaller than lfo_range, change the sign of lfo_step
            if lfo_value > lfo_range:
                lfo_step = -1
            if lfo_value < -lfo_range:
                lfo_step = 1


    ## Send the MIDI CCs ##
    for i in range(0,7):
        new_midi_values[i] += lfo_destination[i] * lfo_value  # add the lfo_output to selected destinations
        # Limit the peaks so the LFO doesn't send MIDI values outside of 0-127
        if new_midi_values[i] > 126:
            new_midi_values[i] = 127
        if new_midi_values[i] < 1:
            new_midi_values[i] = 0
        # Send the new MIDI value, if it has changed
        if current_midi_values[i] != new_midi_values[i]:
            current_midi_values[i] = new_midi_values[i]
            midi.send(ControlChange(midi_cc[i], current_midi_values[i]))

















