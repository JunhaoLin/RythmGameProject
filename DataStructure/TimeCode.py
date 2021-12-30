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
        

        def __init__(self) -> None:
            super().__init__()
    