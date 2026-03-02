class ParkingSession:
    def __init__(self, card_id, entry_time, slot_id):
        self.card_id = card_id
        self.entry_time = entry_time
        self.slot_id = slot_id
        self.exit_time = None
        self.fee = 0