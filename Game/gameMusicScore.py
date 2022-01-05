from typing import Any, Dict, List
from node import ANode
from DataStructure.TimeCode import TimeCodeInMeasures
from DataStructure.util.UtilityClass import meter
from Game.Util.UtilityFunctions import sort_node_list_by_start_time

class pianoGameMusicScore():
    """This class represents the game score that is used by the interactive part of the game
    This score is specifically for piano-like falling pattern.

    Example:
        | ~ |   |   |   |
        |   | ~ |   |   |
        |   |   | ~ |   |
        |   |   |   |   |
        |   | ~ | ~ |   |
       
        - This is a pianoGameMusicScore with 4 trails.
        - Where `~` is a node which will fall down to the line and to be hit by players.
    """

    _all_nodes: List[ANode]
    _meters: Dict[TimeCodeInMeasures, meter]
    _num_trail: int

    def __init__(self, all_nodes: List[ANode], meters: Dict[TimeCodeInMeasures, meter], num_trail: int) -> None:
        self._all_nodes = sort_node_list_by_start_time(all_nodes)
        self._meters = meters
        self._num_trail = num_trail
        if not self.validate_piano_score():
            raise ValueError('Parameters of this object is illegal')
        

    def __hash__(self):
        return hash(self._all_nodes + self._meters)

    def __eq__(self, obj: Any):
        if not isinstance(obj, pianoGameMusicScore):
            return False
        return self._all_nodes == obj._all_nodes \
            and self._meters == obj._meters

    def validate_piano_score(self) -> bool:
        """Method to validate the legality of a pianoGameMusicScore object."""
        for node in self._all_nodes:
            if not isinstance(node, ANode) \
                or node.get_init_trail > self._num_trail:
                return False

        for timecode, meters in zip(list(self._meters.keys()), list(self._meters.values())):
            if not isinstance(timecode, TimeCodeInMeasures) or not isinstance(meters, meter):
                return False

        if not isinstance(self._num_trail, int):
            return False

        return True
 
    def sort_all_nodes_in_score(self) -> None:
        """Method to sort all the nodes in the score according to the start time"""
        sorted_nodes = sort_node_list_by_start_time(self._all_nodes)
        self._all_nodes = sorted_nodes

    def get_note_start_time_in_second(self, specific_node: ANode) -> float:
        """Method to locate the starting time """
        pass
    
        
        

    