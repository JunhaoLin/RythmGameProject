

from typing import Dict, List
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
