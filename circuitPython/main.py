# Pi Pico MIDI controller
print('hello world!')
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

# set up
mux_0.value = False
mux_1.value = False
mux_2.value = False

while True:
    ## Read Potentiometers ##
    # pot 3: 000
    mux_2.value = False
    pot_readings[3] = mux_reading.value >> 9
    time.sleep(SLEEP_TIME)
    # pot 7: 001
    mux_0.value = True
    pot_readings[7] = mux_reading.value >> 9
    time.sleep(SLEEP_TIME)
    # pot 6: 011
    mux_1.value = True
    pot_readings[6] = mux_reading.value >> 9
    time.sleep(SLEEP_TIME)
    # pot 2: 010
    mux_0.value = False
    pot_readings[2] = mux_reading.value >> 9
    time.sleep(SLEEP_TIME)
    # pot 0: 110
    mux_2.value = True
    pot_readings[0] = mux_reading.value >> 9
    time.sleep(SLEEP_TIME)
    # pot 4: 111
    mux_0.value = True
    pot_readings[4] = mux_reading.value >> 9
    time.sleep(SLEEP_TIME)
    # pot 5: 101
    mux_1.value = False
    pot_readings[5] = mux_reading.value >> 9
    time.sleep(SLEEP_TIME)
    # pot 1: 100
    mux_0.value = False
    pot_readings[1] = mux_reading.value >> 9
    time.sleep(SLEEP_TIME)
    #print('midi_values: ', midi_values)

    ## Map Potentiometer Readings to Midi CCs ##
    new_midi_values[0] = pot_readings[0]    # Pot 0: Mod Time
    new_midi_values[1] = pot_readings[1]    # Pot 1: Mod Depth
    new_midi_values[2] = pot_readings[2]    # Pot 2: Delay Time
    new_midi_values[3] = pot_readings[3]    # Pot 3: Delay Depth
    new_midi_values[4] = pot_readings[4]    # Pot 4: Reverb Time
    new_midi_values[6] = pot_readings[6]    # Pot 6: Reverb Mix

    # Pot 5: Base Reverb Depth
    # Pot 7: 'tilt LFO' -> Reverb Depth
    #new_midi_values[5] = pot_readings[5]
    new_midi_values[5] = int((pot_readings[5] + pot_readings[7])/2)
    print('new_midi', new_midi_values)
    # print('pot_readings', pot_readings)

    ## Send the MIDI CCs ##
    for i in range(0,7):
        if current_midi_values[i] != new_midi_values[i]: #send the midi message only if it has changed
            current_midi_values[i] = new_midi_values[i]
            midi.send(ControlChange(midi_cc[i], current_midi_values[i]))

    time.sleep(2.0)
















