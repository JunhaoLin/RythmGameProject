from typing import Any, Dict, List
from node import ANode
from DataStructure.TimeCode import TimeCodeInMeasures
from DataStructure.util.UtilityClass import meter

class gameMusicScore():
    """This class represents the game score that is used by the interactive part of the game"""

    _all_nodes: List[ANode]
    _meters: Dict[TimeCodeInMeasures, meter]

    def __init__(self, all_nodes: List[ANode], meters: Dict[TimeCodeInMeasures, meter]) -> None:
        self._all_nodes = all_nodes
        self._meters = meters

    def __hash__(self):
        return hash(self._all_nodes + self._meters)

    def __eq__(self, obj: Any):
        if not isinstance(obj, gameMusicScore):
            return False
        return self._all_nodes == obj._all_nodes \
            and self._meters == obj._meters

    