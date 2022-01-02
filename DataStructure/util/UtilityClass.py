#stashes all utilities used by data structure

from typing import Any, Tuple, Dict


class meter():
    """The rhythmic pattern of a measure"""

    _num_beats: int
    """How many notes are there in a measure"""

    _beat_unit: int
    """What kinds of notes construct the measure"""

    def __init__(self, num_beats: int, beat_unit: int) -> None:
        if not isinstance(num_beats, int) or not isinstance(beat_unit, int):
            raise ValueError('num_beats and beat_unit must be an integer')
        self._num_beats = num_beats
        self._beat_unit = beat_unit

    def __hash__(self, num_beats: int, beat_unit: int) -> int:
        return hash(self._num_beats + self._beat_unit)

    def __eq__(self, obj: Any) -> bool:
        if not isinstance(obj, meter):
            return False
        return self._beat_unit == obj._beat_unit \
            and self._num_beats == obj._num_beats

    def get_num_beats(self) -> int:
        return self._num_beats

    def get_beat_unit(self) -> int:
        return self._beat_unit
