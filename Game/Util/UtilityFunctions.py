from typing import Any, Dict, List
from DataStructure.TimeCode import TimeCodeInMeasures
from UtilityClass import meter
from node import ANode
from copy import deepcopy
import math

def sort_node_list_by_start_time(loNode: List[ANode]) -> List[ANode]:
    """To sort a list of node based on their starting time in measure-and-beat"""
    sorted_list: List[ANode] = []
    copied_list = loNode
    for i in range(len(loNode)):
        #Execute the amount of time equal to the range of node
        #Everytime, get the earliest node and remove it (linear sort)
        earliest_node = copied_list[0]
        for node_to_compare in copied_list:
            if node_to_compare.get_start_time() < earliest_node.get_start_time():
                earliest_node = node_to_compare
        
        sorted_list.append(earliest_node)
        copied_list.remove(earliest_node)
        
    return sorted_list


def Log2(x):
    """To get the the exponential factor of log base 2 and the input"""
    return (math.log10(x) /
            math.log10(2))


def isPowerOfTwo(n) -> bool:
    """To check if an integer is the power of 2"""
    return (math.ceil(Log2(n)) == math.floor(Log2(n)))


def differenceBetweenTimeInMeasure(t1: TimeCodeInMeasures, t2: TimeCodeInMeasures, mt: meter) -> TimeCodeInMeasures:
    """To find the duration between two time expressed in the format of measures"""

    # The given t2 should not be earlier than t1"
    if t2 < t1:
        raise ValueError('t2 cannot be earlier than t1')
    
    duration_num_measure: int
    duration_num_beat: float

    # Borrowing may happen if the numbeat of t2 is less than that of t1
    if t2.get_num_beat >= t1.get_num_beat:
        duration_num_measure = t2.get_num_measure - t1.get_num_measure
        duration_num_beat = t2.get_num_beat - t1.get_num_beat
    else:
        duration_num_measure = t2.get_num_measure - t1.get_num_measure - 1
        duration_num_beat = mt.get_num_beats + t2.get_num_beat - t1.get_num_beat

    duration = TimeCodeInMeasures(duration_num_measure, duration_num_beat)

    return duration
