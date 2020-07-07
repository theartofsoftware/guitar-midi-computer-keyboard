import time
import keyboard as keyboard_library

from midi_numbers import number_to_note

MIDI_NOTE_TO_KEY_MAP = {
    40: " ",
    72: "(",
    73: "'",
}


class MidiComputerKeyboard:
    def __init__(self, keyboard, timer):
        self.keyboard = keyboard
        self.timer = timer
        self.last_note_on_time = None
        self.shift_on = False

    @classmethod
    def create(cls):
        """Public constructor uses true dependencies"""
        return cls(keyboard_library, time.time)

    def write_note_as_keypress(self, note):
        if note in MIDI_NOTE_TO_KEY_MAP:
            character = MIDI_NOTE_TO_KEY_MAP[note]
        else:
            offset = 24 if self.shift_on else 56
            character = chr(note + offset)

        self.keyboard.write(character)

    def process_guitar_note_off(self, note):
        if self.last_note_on_time is None:
            # Haven't received a 'note_on' message yet
            return

        if self.timer() - self.last_note_on_time < 0.20:
            # Note is too short to be registered
            return

        print(number_to_note(note))
        self.write_note_as_keypress(note)

    def handle_guitar_message(self, message):
        # print(message.dict())
        if message.type == "note_on":
            self.last_note_on_time = self.timer()
        elif message.type == "note_off":
            self.process_guitar_note_off(message.note)

    def handle_pedal_message(self, message):
        if message.type == "control_change" and message.value == 127:
            self.shift_on = True
        elif message.type == "control_change" and message.value == 0:
            self.shift_on = False
