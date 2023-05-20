def calc_available_slots(self):
    """
    This method will set the slot availability based on the maintenance_window.
    This will edit the self.data dict. 
    If the slot is available, the value will be True.
    """
    if self.maintenance_window is None:
        logger.debug('maintenance_window is {}'.format(self.maintenance_window))
        return
    
    blocks = self.maintenance_window.split('+')
    for block in blocks:
        # From (, to everything that's not a )
        times_range = re.search('\\(([^)]+)', block).group(1)
        days_group = block.replace('({})'.format(times_range), '').split('-')
        times_range = times_range.split('-')

        # Convert the time range to seconds starting from epoch
        time_start = int(datetime(1970, 1, 1, 
                                  int(times_range[0].split(':')[0]) % 24, 
                                  int(times_range[0].split(':')[1]) % 60, 0, 0, 
                                  tzinfo=timezone.utc).timestamp())
        time_end = int(datetime(1970, 1, 1, 
                                int(times_range[1].split(':')[0]) % 24,
                                int(times_range[1].split(':')[1]) % 60, 0, 0, 
                                tzinfo=timezone.utc).timestamp())
        time_end = ((time_end - 1) % 86400) + 1  # Fix 24:00 parsed as 00:00
        
        # Checks to avoid infinite loop. In theory is not needed
        time_start = time_start if 0 <= time_start <= 86400 else 0
        time_end = time_end if 0 <= time_end <= 86400 else 86400
        logger.debug('Range: start {} -- end {}'.format(time_start, time_end))

        for day in days_group:
            current_second = time_start
            while current_second < time_end:
                index = (self.NAME_TO_NUM_WEEK[day] - 1) * 86400 + current_second
                self._make_slot_available_if_exists(index)
                current_second += self.RESOLUTION_IN_MINUTE * 60

def _make_slot_available_if_exists(self, slot_index: int):
    if slot_index in self.data:
        self.data[slot_index] = True
    else:
        # If slot_index not exist is better to lower RESOLUTION_IN_MINUTE value
        logger.error('Slot {} does not exist.'.format(slot_index))
