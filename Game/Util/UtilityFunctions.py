from typing import Any, Dict, List
from node import ANode
from copy import deepcopy


def sort_node_list_by_start_time(loNode: List[ANode]) -> List[ANode]:
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

    

def sort_node_list_by_start_time_inseconds(list_nodes: List[ANode]) -> List[ANode]:
    list_timecode = []
    list_seconds = []
    for node in list_nodes:
        list_timecode.append(node.get_start_time())
    
    for timecodes in list_timecode:
        pass