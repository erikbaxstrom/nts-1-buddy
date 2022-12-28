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

mux_0.value = False
mux_1.value = False
mux_2.value = False

lfo_last_update = time.monotonic()
lfo_step = -1
lfo_range = 15
lfo_value = 0
lfo_output = 0

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
    # Translate pot 7 to a time interval
    lfo_update_interval = 0.001 + 0.005*pot_readings[7]/8 # minimum 0.01 seconds between change plus 0 to 128*2*10 milliseconds
    lfo_range = pot_readings[7] >> 2

    # Is it time yet?
    if time.monotonic() >= (lfo_last_update + lfo_update_interval):
        lfo_last_update = time.monotonic()
        lfo_value += lfo_step
        lfo_output = pot_readings[5] + lfo_value
        #new_midi_values[5] = lfo_output


        # If lfo_value is bigger or smaller than lfo_range, change the sign of lfo_step
        if lfo_value > lfo_range:
            lfo_step = -1
        if lfo_value < -lfo_range:
            lfo_step = 1
        # Limit the peaks so the LFO doesn't take the output outside of 0-127
        if lfo_output > 126:
            #lfo_step = -1 #limit the LFO range (breaks when pot5 is adjusted while lfo_value is peaking
            lfo_output = 127 #clip the LFO waveform
        if lfo_output < 1:
            #lfo_step = 1
            lfo_output = 0
        #new_midi_values[5] = pot_readings[5] + lfo_value
    new_midi_values[5] = lfo_output
    #print('midi_out[5]', new_midi_values[5])
    #new_midi_values[5] = pot_readings[5] + lfo_value
    #print('new_midi', new_midi_values, 'lfo_value', lfo_value)


    # print('pot_readings', pot_readings)

    ## Send the MIDI CCs ##
    for i in range(0,7):
        if current_midi_values[i] != new_midi_values[i]: #send the midi message only if it has changed
            current_midi_values[i] = new_midi_values[i]
            midi.send(ControlChange(midi_cc[i], current_midi_values[i]))

    #time.sleep(0.2)
















