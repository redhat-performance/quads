class Outlets(object):
    def __init__(self,uid):
        self.uid = uid
        self.name = None
        self.description = None
        self.state = None
        self.brands = [ "ServerTech","Apc" ]
    def get_brands(self):
        return self.brands
    def set_name(self, name):
        self.name = name
    def set_description(self, desc):
        self.description = desc
    def set_state(self, state):
        self.state = state
    def get_state(self):
        return self.state
    def get_id(self):
        return self.uid
    def get_name(self):
        return self.name
    def get_desc(self):
        return self.description
