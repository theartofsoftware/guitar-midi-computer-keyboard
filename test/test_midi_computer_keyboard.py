import pytest
import mido
from midi_computer_keyboard import MidiComputerKeyboard


class MockKeyboard:
    def __init__(self):
        self.pressed_keys = []

    def write(self, key):
        self.pressed_keys.append(key)


class MockTimer():
    def __init__(self):
        self.count = 0

    def advance(self, seconds):
        self.count += seconds

    def __call__(self):
        return self.count


def midi(data):
    return mido.Message.from_dict(data)


@pytest.fixture
def mock_keyboard():
    return MockKeyboard()


@pytest.fixture
def mock_timer():
    return MockTimer()


@pytest.fixture
def midi_computer_keyboard(mock_keyboard, mock_timer):
    return MidiComputerKeyboard(mock_keyboard, mock_timer)


def test_lower_case_letter(mock_keyboard, mock_timer, midi_computer_keyboard):
    midi_computer_keyboard.handle_guitar_message(
        midi({"type": "note_on", "note": 43})
    )
    mock_timer.advance(1)
    midi_computer_keyboard.handle_guitar_message(
        midi({"type": "note_off", "note": 43})
    )

    assert mock_keyboard.pressed_keys == ["c"]


def test_upper_case_letter(mock_keyboard, mock_timer, midi_computer_keyboard):
    midi_computer_keyboard.handle_pedal_message(
        midi({"type": "note_on", "note": 43})
    )
    midi_computer_keyboard.handle_guitar_message(
        midi({"type": "note_on", "note": 43})
    )
    mock_timer.advance(1)
    midi_computer_keyboard.handle_guitar_message(
        midi({"type": "note_off", "note": 43})
    )

    assert mock_keyboard.pressed_keys == ["C"]


def test_case_toggling_using_pedal(mock_keyboard, mock_timer, midi_computer_keyboard):
    # Shift on
    midi_computer_keyboard.handle_pedal_message(
        midi({"type": "note_on", "note": 43})
    )
    midi_computer_keyboard.handle_guitar_message(
        midi({"type": "note_on", "note": 43})
    )
    mock_timer.advance(1)
    midi_computer_keyboard.handle_guitar_message(
        midi({"type": "note_off", "note": 43})
    )
    mock_timer.advance(1)

    # Shift off
    midi_computer_keyboard.handle_pedal_message(
        midi({"type": "note_on", "note": 43})
    )
    midi_computer_keyboard.handle_guitar_message(
        midi({"type": "note_on", "note": 43})
    )
    mock_timer.advance(1)
    midi_computer_keyboard.handle_guitar_message(
        midi({"type": "note_off", "note": 43})
    )

    assert mock_keyboard.pressed_keys == ["C", "c"]


def test_e2_translates_into_a_space(
    mock_keyboard, mock_timer, midi_computer_keyboard
):
    midi_computer_keyboard.handle_guitar_message(
        midi({"type": "note_on", "note": 40})
    )
    mock_timer.advance(1)
    midi_computer_keyboard.handle_guitar_message(
        midi({"type": "note_off", "note": 40})
    )

    assert mock_keyboard.pressed_keys == [" "]


def test_short_notes_arent_registered(
    mock_keyboard, mock_timer, midi_computer_keyboard
):
    midi_computer_keyboard.handle_guitar_message(
        midi({"type": "note_on", "note": 40})
    )
    mock_timer.advance(0.1)
    midi_computer_keyboard.handle_guitar_message(
        midi({"type": "note_off", "note": 41})
    )

    assert mock_keyboard.pressed_keys == []
