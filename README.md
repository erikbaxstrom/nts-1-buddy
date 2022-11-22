# nts-1-buddy

A MIDI controller and companion for my Korg NTS-1. The NTS-1 is powerful, but with only two control knobs, it's hard to adjust the effects in real time. I primarily use the effects (not the synth) so a keyboard is unnecessary. Commercially available MIDI controllers are often expensive, bulky, or not directly compatible with Serial MIDI.

## Concept

MIDI controller that's compact (about the same size as the NTS-1) and can control and/or modulate parameters through MIDI CC.

Aim to use inexpensive, widely available components.

### NTS-1 MID Parameters

Effects

- Mod: time, depth
- Delay: time, depth, mix\*
- Reverb: time, depth, mix\*

Synth

- Oscillator: shape, alt
- Envelope: AR
- Filter Sweep: rate, depth\*
- Arp: pattern, interval, length
- Tremollo

### Ideas For Effects Modulation

- Hammondeggs reverbs use HP or LP filters. Modulate that w/ an LFO could be cool.
- Delay time. Changing the delay time while the delay is playing can make interesting sounds.

# Proof of Concept Phase

## Select Hardware -- Complete

- Raspberry Pi Pico. Because it's inexpensive, powerful, has lots of i/o, and I already have several of them to experiment with.

- 8x rotary potentiometers
- 4x push buttons
- 3.5mm TRS MIDI cable Type A -- same type as the NTS-1
- 8x Multiplexer to read the 8 pots b/c the Pico only has three analog inputs

## Experiment With Delay Modulation (using pure data) -- Complete

Twisting the time parameter knob on the NTS-1 while the delay is playing does interesting things to the sound, but it can be hard to control. Maybe it's possible to control this programmatically.

### Does doubling the MIDI CC Value Double the Delay Time?

nope. Speed of change in time parameter translates to pitch. Not as straightforward or musically useful as I had hoped, but…

### Can the Delay Time be Modulated Quickly With an AD (or other) Envelope?

Yes, and it can create some interesting glitchy noises or even pitched noises. Seems like there’s some promising stuff here.

### Delay Experiments Conclusion

I will include buttons in the hardware layout. Even without delay modulation effects, the buttons will likely be useful for other things, like sending CC messages to the arpeggiator, selecting an LFO destination (within the controller), or for doing preprogrammed arpeggios, or other things I have yet to dream up. Will want to come back to this after completing MVP.

### Some Ideas Resulting From Delay Experiments

- Maybe buttons can trigger glitches, where the controller steps through a sequence of CC values.

- Taking clock input from the NTS-1 could allow interesting glitch-type sounds in time w/ the clock. This will require an opto-isolator, and probably also some more complex logic (for example, does the glitch trigger every time there's a clock signal? does it keep track of the tempo? I don't remember if the Pico has interrupts, so this will require more research.)

- Delay time can be modulated with depth turned down then depth turned up. This give a little bit less "glitchy" sound than modulating the time without changing the depth. Need more experimentation to see what sounds good.

Modulation of time parameter should be relative to current position of the controller knob, and it should probably reset to the value from the knob position.

— Buttons could set 'modes' for the LFOs or for the delay and then knob function would change based on current mode.

- I really like the Smoke delay from Roll-log, but the NTS-1 can't do user delay at the same time as user reverb, so I'm still hoping to get some more interesting textures out of the built-in delay types.

## Install Firmware and IDE -- complete

- Install Mu
- Download and Install circuitpytjon (circuitpython.org) on Pi Pico:
  - Hold down bootsel button and plug in usb.
  - Hold down until drive appears on laptop.
  - Copy uf2 file onto drive. Confirm drive remounts as “circuitpy”.
- Run a blink LED script.

## Hardware -- complete

- Confirm that I can drill or dremel the perfboard to fit the potentiometer support legs.

## Test MIDI

- Use MIDI over UART to “blink” a note on and off.
- Use MIDI to "blink" a CC over UART
- Maybe, if I'm feeling like it: Breadboard a pot, read value and map to midi cc

# Minimum Viable Product Phase

## Hardware

- Finalize layout and button/pot spacing
- Score and cut perfboard
- Drill out bracket holes for pots
- Solder pots GND together and 3v3 together
- Solder each center pin of pot to DuPont connector lead
- Solder GND and 3v3 to connectors
- Attach standoffs to perf board
- Connect pots to mux
- Connect MUX to RasPi

## Firmware

- Read MUX (using Gray Codes if I'm feeling fancy), convert readings to 8bit, and store in an array
- Send the values in the array as MIDI CC out through UART.
