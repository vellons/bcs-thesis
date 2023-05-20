# Calc the order used to try to schedule all servers. 
# Based on the number of hour available for the update
# the server with more hour available 
# (or maintenance_window==None) it will be scheduled last

self.collect_items_data()
self.calendar = HotfixCalendar(
    int(self.campaign.start_at.timestamp()),
    int(self.campaign.end_at.timestamp()),
    self.SLOT_DURATION_IN_MINUTE,  # Will be 30 minutes
    self.SLOT_MAX_ELEMENTS  # Will be 5 item
)
self.calc_items_priority_score()
self.calc_dependencies_tree()

...

server_key_in_order = sorted(
    self.items_data.keys(),
    key=lambda k: self.items_data[k].priority_score,
)
server_key_not_found_a_schedule = []

for key in server_key_in_order:
    server = self.items_data[key]
    server.slot_start = None
    ...

    available_slots = self.calendar.get_list_of_slot_to_try(server)
    for slot_start in available_slots:
        is_slot_ok = server.is_slot_ok_for_maintenance(
            slot_start, slot_start + self.SLOT_DURATION_IN_MINUTE * 60 - 1
        )
        if is_slot_ok:
            server.apply_slot(slot_start)
            self.calendar.add_to_calendar(slot_start, server)
            break

    # If a slot was not found ServerItem.slot_start is None
    if server.slot_start is None and server.to_schedule:
        server_key_not_found_a_schedule.append(key)

    ...
