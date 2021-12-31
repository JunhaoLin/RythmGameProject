# This is the data representation of the time of the note according to measure（音节）

from abc import ABCMeta, abstractmethod
from typing import Any


class ITimeCode(metaclass = ABCMeta):
    """This is the general interface to represent the time for notes"""

    @abstractmethod
    def get_time_in_seconds(self) -> float:
        """To get the exact time in the format of seconds"""
        raise NotImplementedError
    
    @abstractmethod
    def get_time_in_measure(self, bpm: int) -> tuple:
        """To get the exact time in the format of measure-beat"""
        raise NotImplementedError


class TimeCodeInSeconds(ITimeCode):
    """Concrete implementation of a TimeCode, where we can represents this timecode in seconds."""
    
    _num_second: float
    """Number of seconds from the start of the score"""

    def __init__(self, num_second) -> None:
        self._num_second = num_second

    def __hash__(self):
        return hash(self._num_second)
    
    def __eq__(self, obj: Any) -> bool:
        if not isinstance(obj, TimeCodeInSeconds):
            return False
        return self._num_second == obj._num_second
    
    def get_time_in_seconds(self) -> float:
        return self._num_second
    
    def get_time_in_measure(self, bpm: int) -> tuple:
        #TODO
        pass


class TimeCodeInMeasures(ITimeCode):
    """Concrete implementation of a TimeCode, in MIDI format of measure-beat"""

    _num_measure: int
    """Number of measure"""

    _num_beat: float
    """Number of beats"""

    def __init__(self, num_measure, num_beat) -> None:
        self._num_measure = num_measure
        self._num_beat = num_beat
    
    def __hash__(self):
        return hash(self._num_beat + self._num_measure)

    def __eq__(self, obj: Any) -> bool:
        if not isinstance(obj, TimeCodeInMeasures):
            return False
        return self._num_beat == obj._num_beat and self._num_measure == obj._num_measure

    def __lt__(self, other):
        if self._num_measure < other._num_measure:
            return True
        elif self._num_measure == other._num_measure:
            return self._num_beat < other._num_beat
        else:
            return False

    def __gt__(self, other):
        if self._num_measure > other._num_measure:
            return True
        elif self._num_measure == other._num_measure:
            return self._num_beat > other._num_beat
        else:
            return False
        
    def get_time_in_seconds(self) -> float:
        #TODO
        pass

    def get_time_in_seconds(self) -> float:
        return (self._num_measure, self._num_beat)
    