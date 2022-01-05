# This is the class for nodes

from abc import ABCMeta, abstractmethod
from typing import Any, Dict, List, Type

from DataStructure.TimeCode import TimeCodeInSeconds, TimeCodeInMeasures



class INode(metaclass=ABCMeta):
    """ This component represents the Node of the game.
    * A node is a key where player needs to react when it falls on the line
    - Example:
        Regurlar Node: player only needs to click once
        Hold Node: player needs to hold the key for a while
    """
    
    @abstractmethod
    def missed(self) -> None:
        """Method that decides this node was missed by the player"""
        raise NotImplementedError

    @abstractmethod
    def got_hit(self) -> None:
        """Method that decides this node was hit by the player"""
        raise NotImplementedError

class ANode(INode):
    """The abstract class for node, where common features and functionalities are placed
    """

    _hit: bool
    """hit represents whether this node was hit by the player"""

    _start_time: TimeCodeInMeasures
    """starting time for this node, used to check if player should hit this node"""

    _end_time: TimeCodeInMeasures
    """ending time for this node, used to check if player should release key"""

    _init_trail: int
    """initial trail of the node, to differentiate between nodes from other trails"""

    def __init__(self, start: TimeCodeInMeasures, end: TimeCodeInMeasures, init_trail: int) -> None:
        if not isinstance(start, TimeCodeInMeasures):
            raise TypeError('start must be a TimeCodeInMeasure')
        if not isinstance(end, TimeCodeInMeasures):
            raise TypeError('end must be a TimeCodeInMeasure')
        if not isinstance(init_trail, int):
            raise TypeError('init_trial must be an integer')
        if start > end:
            raise ValueError('starting time can not be latter than ending time')
        if init_trail < 1:
            raise ValueError('note init trail number cannot be negative or zero')
        self._start_time = start
        self._end_time = end
        self._init_trail = init_trail
    
    def __hash__(self):
        return hash(self._hit + self._start_time + self._end_time + self._init_trail)

    def __eq__(self, obj: Any) -> bool:
        if not isinstance(obj, ANode):
            return False
        return self._hit == obj._hit \
            and self._start_time == obj._start_time \
            and self._end_time == obj._end_time \
            and self._init_trail == obj._init_trail

    def missed(self) -> None:
        self._hit = False

    def got_hit(self) -> None:
        self._hit = True

    # getters for class fields
    def get_hit(self) -> bool:
        return self._hit

    def get_start_time(self) -> TimeCodeInMeasures:
        return self._start_time

    def get_end_time(self) -> TimeCodeInMeasures:
        return self._end_time

    def get_init_trail(self) -> int:
        return self._init_trail



    




