# This is the data representation of the time of the note according to measure（音节）

from abc import ABCMeta, abstractmethod
from typing import Any
from UtilityClass import meter
import math


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
    
    def get_time_in_measure(self, num_second: float, bpm: float, mt: meter) -> tuple:
        """Method which convert time in seconds into measure. Parameter should be provided by score."""
        #The duration of one single measure
        time4oneMeasure = (240/bpm) * (mt.get_num_beats() / mt.get_beat_unit())

        #Calculate how many complete measures there are
        num_measure = math.floor(num_second / time4oneMeasure)

        #The duration for remaining beats in the current measure
        time4beats = num_second % time4oneMeasure

        #The duration of one single beat
        time4oneBeat = (240/bpm) / mt.get_beat_unit()

        #Calculate the exact beat of this note
        num_beat = time4beats / time4oneBeat

        #Return the time code in measure
        return (num_measure, num_beat)

        

class TimeCodeInMeasures(ITimeCode):
    """Concrete implementation of a TimeCode, in MIDI format of measure-beat"""

    _num_measure: int
    """Number of measure"""

    _num_beat: float
    """Number of beats"""

    def __init__(self, num_measure: int, num_beat: float) -> None:
        if not isinstance(num_measure, int) or not isinstance(num_beat, float):
            raise TypeError('_num_beat must be an integer / _num_beat must be an float')
        self._num_measure = num_measure
        self._num_beat = num_beat
    
    def __hash__(self):
        return hash(self._num_beat + self._num_measure)

    def __eq__(self, obj: Any) -> bool:
        if not isinstance(obj, TimeCodeInMeasures):
            return False
        return self._num_beat == obj._num_beat and self._num_measure == obj._num_measure

    def __lt__(self, other: Any):
        if self._num_measure < other._num_measure:
            return True
        elif self._num_measure == other._num_measure:
            return self._num_beat < other._num_beat
        else:
            return False

    def __gt__(self, other: Any):
        if self._num_measure > other._num_measure:
            return True
        elif self._num_measure == other._num_measure:
            return self._num_beat > other._num_beat
        else:
            return False
        
    def get_time_in_seconds(self, num_measure: int, num_beat: float, bpm: float, mt: meter) -> float:
        return (240/bpm) * ((mt.get_num_beats() * num_measure / mt.get_beat_unit()) + (num_beat / mt.get_beat_unit()))

    def get_time_in_seconds(self) -> float:
        return (self._num_measure, self._num_beat)
    