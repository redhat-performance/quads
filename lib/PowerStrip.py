class PowerStrip(object):
    def __init__(self,uid):
        self.uid = uid
        self.name = None
        self.description = None
        self.state = None
        self.wattage = None
        self.amps = None
        self.volts = None
    def set_name(self, name):
        self.name = name
    def set_description(self, desc):
        self.description = desc
    def set_state(self, volts,amps, watts):
        self.volts = volts
        self.wattage = watts
        self.amps = amps
    def get_state(self):
        return self.volts,self.amps,self.wattage
    def get_id(self):
        return self.uid
    def get_name(self):
        return self.name
    def get_desc(self):
        return self.description
