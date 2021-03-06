from typing import Any, Dict, List
from node import ANode
from DataStructure.TimeCode import TimeCodeInMeasures
from DataStructure.util.UtilityClass import meter
from Game.Util.UtilityFunctions import sort_node_list_by_start_time, differenceBetweenTimeInMeasure

class pianoGameMusicScore():
    """This class represents the game score that is used by the interactive part of the game
    This score is specifically for piano-like falling pattern.
    In the default case, the meter and the bpm is fixed throughout the entire music.

    Example:
        | ~ |   |   |   |
        |   | ~ |   | ~ |
        |   |   | ~ |   |
        |   |   |   |   |
        |   | ~ | ~ |   |
       
        - This is a pianoGameMusicScore with 4 trails.
        - Where `~` is a node which will fall down to the line and to be hit by players.
    """

    # -------------- Fields ----------------
    _all_nodes: List[ANode]
    _num_trail: int
    _fix_meter: meter
    _fix_bpm: float

    _node_start_time_in_seconds: Dict[ANode, float]
    _node_end_time_in_seconds: Dict[ANode, float]
    

    # ------------ Constructor -------------
    def __init__(self, all_nodes: List[ANode], num_trail: int, fix_meter: meter, fix_bpm: float) -> None:
        self._all_nodes = sort_node_list_by_start_time(all_nodes)
        self._num_trail = num_trail
        self._fix_meter = fix_meter
        self._fix_bpm = fix_bpm
        
        self._node_start_time_in_seconds = self.get_all_node_start_time_in_second()
        self._node_end_time_in_seconds = self.get_all_node_end_time_in_second()

        if not self.validate_piano_score():
            raise ValueError('Some parameter(s) given to this object are not legal')
        

    # -------------- Methods ---------------
    def __hash__(self):
        return hash(self._all_nodes + self._num_trail + self._fix_meter + self._fix_bpm)


    def __eq__(self, obj: Any):
        if not isinstance(obj, pianoGameMusicScore):
            return False
        return self._all_nodes == obj._all_nodes \
            and self._num_trail == obj._num_trail \
            and self._fix_meter == obj._fix_meter \
            and self._fix_bpm == obj._fix_bpm


    def validate_piano_score(self) -> bool:
        """Method to validate the legality of a pianoGameMusicScore object."""

        for node in self._all_nodes:
            if not isinstance(node, ANode) \
                or node.get_init_trail > self._num_trail:
                return False

        if not isinstance(self._num_trail, int):
            return False

        if not isinstance(self._fix_meter, meter):
            return False

        if not isinstance(self._fix_bpm, float):
            return False

        return True
 

    def sort_all_nodes_in_score(self) -> None:
        """Method to sort all the nodes in the score according to the start time"""
        sorted_nodes = sort_node_list_by_start_time(self._all_nodes)
        self._all_nodes = sorted_nodes


    def get_all_node_start_time_in_second(self) -> Dict[ANode, float]:
        """Method to come up with a dictionary indicating the starting time (in seconds) of all nodes"""
        node_start_seconds: Dict[ANode, float]
        
        for node in self._all_nodes:
            node_start_seconds[node] = self.get_note_start_time_in_second(node)

        return node_start_seconds


    def get_all_node_end_time_in_second(self) -> Dict[ANode, float]:
        """Method to come up with a dictionary indicating the ending time (in seconds) of all nodes"""
        node_end_seconds: Dict[ANode, float]

        for node in self._all_nodes:
            node_end_seconds[node] = self.get_note_end_time_in_second(node)
            
        return node_end_seconds


    def retrieve_all_node_start_time(self) -> Dict[ANode, float]:
        """The getter for the start-time-in-second dictionary"""
        return self._node_start_time_in_seconds


    def retrieve_all_node_end_time(self) -> Dict[ANode, float]:
        """The getter for the end-time-in-second dictionary"""
        return self._node_end_time_in_seconds


    def get_note_start_time_in_second(self, specific_node: ANode) -> float:
        """Method to locate the starting time of a node in seconds"""
        return self.get_time_in_second(specific_node.get_start_time())


    def get_note_end_time_in_second(self, specific_node: ANode) -> float:
        """Method to locate the ending time of a node in seconds"""
        return self.get_time_in_second(specific_node.get_end_time())


    def get_time_in_second(self, t_in_measure: TimeCodeInMeasures) -> float:
        """Method to locate a specific time in seconds using a time code in measures"""

        # The following would be an transformation equation used for all fix-meter, fix-bpm music
        num_measure = t_in_measure.get_num_measure()
        num_beat = t_in_measure.get_num_beat()

        return (240 / self._fix_bpm) * (self._fix_meter.get_num_beats() / self._fix_meter.get_beat_unit()) \
            * (num_measure + (num_beat / self._fix_meter.get_num_beats()))

    
        

class VBPMPianoGameMusicScore(pianoGameMusicScore):
    """
    A specific kind of pianoGameMusicScore which have fix meter but changing bpm
    For instance:
    bpm  120              90                    80  70  60  50 ...
    4/4  ||   |   |   |   ||   |   |   |   ||   |   |   |   || ...
    """

    # --------------- Fields -----------------
    _all_nodes: List[ANode]
    _num_trail: int
    _fix_meter: meter
    _var_bpm: Dict[TimeCodeInMeasures, float]

    _node_start_time_in_seconds: Dict[ANode, float]
    _node_end_time_in_seconds: Dict[ANode, float]


    # ------------- Constructor --------------
    def __init__(self, all_nodes: List[ANode], num_trail: int, fix_meter: meter, \
        var_bpm: Dict[TimeCodeInMeasures, float]) -> None:
        self._all_nodes = sort_node_list_by_start_time(all_nodes)
        self._num_trail = num_trail
        self._fix_meter = fix_meter
        # !Note!: the first bpm must be at the start, the last bpm should not exceed end of last node
        self._var_bpm = var_bpm
        
        self._node_start_time_in_seconds = self.get_all_node_start_time_in_second()
        self._node_end_time_in_seconds = self.get_all_node_end_time_in_second()

        if not self.validate_piano_score():
            raise ValueError('Parameters of this object is illegal')


    # --------- Overwritten methods ----------
    def __hash__(self):
        return hash(self._all_nodes, self._num_trail, self._fix_meter, self._var_bpm)


    def __eq__(self, obj: Any):
        if not isinstance(obj, VBPMPianoGameMusicScore):
            return False
        return self._all_nodes == obj._all_nodes \
            and self._num_trail == obj._num_trail \
            and self._fix_meter == obj._fix_meter \
            and self._var_bpm == obj._var_bpm


    def validate_piano_score(self) -> bool:
        """Method to validate the legality of a pianoGameMusicScore object."""
        for node in self._all_nodes:
            if not isinstance(node, ANode) \
                or node.get_init_trail > self._num_trail:
                return False

        if not isinstance(self._num_trail, int):
            return False
       
        if not isinstance(self._fix_meter, meter):
            return False

        if self._var_bpm.__len__ == 0:   #### length??????????????????
            return False

        for timecode, bpms in zip(list(self._var_bpm.keys()), list(self._var_bpm.values())):
            if not isinstance(timecode, TimeCodeInMeasures) or not isinstance(bpms, float):
                return False

        first_bpm_time = list(self._var_bpm.keys())[0]

        if first_bpm_time.get_num_measure != 0 or first_bpm_time.get_num_beat != 0.0:
            return False

        return True


    def get_time_in_second(self, t_in_measure: TimeCodeInMeasures) -> float:
        
        # The algorithim adds up time in second before every new change of bpm
        total_t_in_second: float
        total_t_in_second = 0.0

        all_bpm_location: List[TimeCodeInMeasures]
        all_bpm_location = self._var_bpm.keys()
        all_bpm_location.append(t_in_measure)

        all_bpm_value: List[float]
        all_bpm_value = self._var_bpm.values()
        
        i = 0
        while i < all_bpm_value.__len__:     #### length?????????????????????
            section_t_in_second: float
            # this stands for the duration of a particular section of bpm

            current_bpm = all_bpm_value[i]
            duration = differenceBetweenTimeInMeasure(all_bpm_location[i], all_bpm_location[i + 1], self._fix_meter)
            section_t_in_second = (240 / current_bpm) * (self._fix_meter.get_num_beats() / self._fix_meter.get_beat_unit) \
                * (duration.get_num_measure() + (duration.get_num_beat() / self._fix_meter.get_num_beats()))

            total_t_in_second = total_t_in_second + section_t_in_second        

        return total_t_in_second

    

class VMVBPianoGameMusicScore(VBPMPianoGameMusicScore):
    """
    A specific kind of VBPMPianoGameMusicScore which have changing bpm and meter
    For instance:
    bpm   120              90                80  70  60  50 ...
          ||   |   |   |   ||   |   |   ||   |   ||   |   || ...
    meter 4/4              3/4          2/4        
    """

    # --------------- Fields -----------------
    _all_nodes: List[ANode]
    _num_trail: int
    _var_meter: Dict[TimeCodeInMeasures, meter]
    # !Note!: meter change can only happen at start of measures
    _var_bpm: Dict[TimeCodeInMeasures, float]

    _node_start_time_in_seconds: Dict[ANode, float]
    _node_end_time_in_seconds: Dict[ANode, float]


    # ------------- Constructor --------------
    def __init__(self, all_nodes: List[ANode], num_trail: int, var_meter: Dict[TimeCodeInMeasures, meter], \
        var_bpm: Dict[TimeCodeInMeasures, float]) -> None:
        self._all_nodes = sort_node_list_by_start_time(all_nodes)
        self._num_trail = num_trail
        self._var_meter = var_meter
        self._var_bpm = var_bpm
        
        self._node_start_time_in_seconds = self.get_all_node_start_time_in_second()
        self._node_end_time_in_seconds = self.get_all_node_end_time_in_second()

        if not self.validate_piano_score():
            raise ValueError('Parameters of this object is illegal')

        self.fufill_var_meter()

    
    # --------- Overwritten methods ----------
    def __hash__(self):
        return hash(self._all_nodes, self._num_trail, self._var_meter, self._var_bpm)

    def __eq__(self, obj: Any):
        if not isinstance(obj, VMVBPianoGameMusicScore):
            return False
        return self._all_nodes == obj._all_nodes \
            and self._num_trail == obj._num_trail \
            and self._var_meter == obj._var_meter \
            and self._var_bpm == obj._var_bpm

    def validate_piano_score(self) -> bool:
        """Method to validate the legality of a pianoGameMusicScore object."""
        for node in self._all_nodes:
            if not isinstance(node, ANode) \
                or node.get_init_trail > self._num_trail:
                return False

        if not isinstance(self._num_trail, int):
            return False
       
        if self._var_meter.__len__ == 0:   #### length??????????????????
            return False

        if self._var_bpm.__len__ == 0:   #### length??????????????????
            return False

        for timecode, meters in zip(list(self._var_meter.keys()), list(self._var_meter.values())):
            if not isinstance(timecode, TimeCodeInMeasures) or not isinstance(meters, meter):
                return False

        for timecode, bpms in zip(list(self._var_bpm.keys()), list(self._var_bpm.values())):
            if not isinstance(timecode, TimeCodeInMeasures) or not isinstance(bpms, float):
                return False
            # Change in meter can only at the start of measures
            if not timecode.get_num_beat() == 0.0:
                return False

        first_meter_time = list(self._var_bpm.keys())[0]

        if first_meter_time.get_num_measure != 0 or first_meter_time.get_num_beat != 0.0:
            return False

        first_bpm_time = list(self._var_bpm.keys())[0]

        if first_bpm_time.get_num_measure != 0 or first_bpm_time.get_num_beat != 0.0:
            return False

        return True


    def get_time_in_second(self, t_in_measure: TimeCodeInMeasures) -> float:

        # This algorithm adds up every section
        # The section is constructed by every change in bpm or meter
        total_t_in_second: float
        total_t_in_second = 0.0

        # Get the location of every bpm change
        all_bpm_location: List[TimeCodeInMeasures]
        all_bpm_location = self._var_bpm.keys()
        #all_bpm_location.append(t_in_measure)

        # Get the value of every bpm change
        all_bpm_value: List[float]
        all_bpm_value = self._var_bpm.values()

        # Get the location of every meter change
        all_meter_location: List[TimeCodeInMeasures]
        all_meter_location = self._var_meter.keys()

        # Get the value of every meter change
        all_meter_value: List[float]
        all_meter_value = self._var_meter.values()

        # Synchronize the two dictionaries
        # For every change for bpm where there is no change of meter, add the same previous meter


        # For every change for meter where there is no change of bpm, add the same previous bpm


        return total_t_in_second

    
    def fufill_var_meter(self) -> None:
        """
        Fufill the var-meter field of the class.
        Example:
        Total: 10 measures (last measure noted as measure No.9)
        (0, 0): 4/4
        (4, 0): 2/4
        (6, 0): 3/4
        (9, 0): 4/4
            ???
        (0, 0): 4/4
        (1, 0): 4/4
        (2, 0): 4/4
        (3, 0): 4/4
        (4, 0): 2/4
        (5, 0): 2/4
        (6, 0): 3/4
        (7, 0): 3/4
        (8, 0): 3/4
        (9, 0): 4/4
        
        """
        fufilled_var_meter: Dict[TimeCodeInMeasures, meter]

        # Get the total number of measures
        num_measure_in_total: int
        num_measure_in_total = self._all_nodes[(self._all_nodes.__len__) - 1].get_end_time().get_num_measure()
        #### length??????????????????

        # Make a copy of the original var_bpm field
        var_meter_copy: Dict[TimeCodeInMeasures, meter]
        var_meter_copy = self._var_meter

        # Use a list to collect all the measure number that involve a bpm change
        all_measure_vmeter = var_meter_copy.keys()
        
        i = 0
        while i < all_measure_vmeter.__len__:
            # Get the current change in meter
            current_vmeter_measure = all_measure_vmeter[i]
            current_vmeter_value = var_meter_copy.get(current_vmeter_measure)

            # Write it down
            fufilled_var_meter[current_vmeter_measure] = current_vmeter_value

            # Fill the value forward until the next change or the end
            j = current_vmeter_measure + 1

            # If this is not the last one in the list
            if not (i == all_measure_vmeter.__len__ - 1):
                # Find the next item in the list, decide how many times to copy this meter value
                next_vmeter_measure = all_measure_vmeter[i + 1]
                while j < next_vmeter_measure:
                    fufilled_var_meter[j] = current_vmeter_value
            # If this is the last one in the list
            else:
                # Copy the last meter value until the last measure of this 
                while j <= num_measure_in_total:
                    fufilled_var_meter[j] = current_vmeter_value

        
        self._var_meter = fufilled_var_meter

        