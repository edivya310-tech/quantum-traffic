from app.schemas.signals import SignalSchema

class FixedTimeController:
    def __init__(self, config):
        self.config = config
        
    def get_signal_plan(self, network_state):
        # A simple fixed time strategy that just cycles
        return {}
