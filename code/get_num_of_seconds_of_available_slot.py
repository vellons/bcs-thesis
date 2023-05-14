def get_num_of_seconds_of_available_slot(self, start_range: int = 0, 
                                         end_range: int = 604800) -> int:
    """
    Based on calculated date this function return the number of seconds
    of availability (in a week) for this maintenance window
    :param start_range: default 0 that means from monday 00:00
    :param end_range: default 604800 that means from sunday 24:00
    :return: number of seconds of availability for this maintenance window
    """
    sum_of_seconds = 0
    while start_range < end_range:
        index = start_range
        if index in self.data:
            if self.data[index] is True:
                sum_of_seconds += self.RESOLUTION_IN_MINUTE * 60  
        start_range += self.RESOLUTION_IN_MINUTE * 60
    return sum_of_seconds
