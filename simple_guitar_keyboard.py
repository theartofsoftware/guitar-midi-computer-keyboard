import mido
from midi_computer_keyboard import MidiComputerKeyboard

MIDI_PEDAL_DEVICE = 'E-MU Xmidi 2x2 0'
MIDI_GUITAR_DEVICE = "loopMIDI Port 2"


def main():
    midi_qwerty = MidiComputerKeyboard.create()
    with mido.open_input(MIDI_GUITAR_DEVICE) as guitar_port, mido.open_input(MIDI_PEDAL_DEVICE) as pedal_port:
        while True:
            guitar_message = guitar_port.poll()
            if guitar_message:
                midi_qwerty.handle_guitar_message(guitar_message)
            pedal_message = pedal_port.poll()
            if pedal_message:
                midi_qwerty.handle_pedal_message(pedal_message)


if __name__ == "__main__":
    main()
