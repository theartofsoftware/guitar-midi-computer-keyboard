# MIDI Computer Keyboard

This is a small Python application that converts MIDI messages into computer
keystrokes. It's completely pointless but fun!

It uses two libraries: `mido` for reading MIDI messages, and `keyboard` for performing the keystrokes.

Here's a video I made demonstrating it in action: https://www.youtube.com/watch?v=4rbp83fJTkg

I've only tested that this works on Windows.

I used LoopMIDI to create virtual MIDI ports, and a VST plugin called Migic to convert
the audio signal from my guitar into MIDI messages. These messages are then routed
to LoopMIDI, which pipes the messages to this application.

## Installation

With poetry:

```
> poetry install
```

With Pip:

```
> pip install
```

## Test

```
> pytest
```
