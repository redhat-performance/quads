import PowerManagement
import Outlets
import PowerStrip
import Connect
import time
import re
import logging

class ServerTech(PowerManagement.PowerManagement):

    def __init__(self,user,password,host,options={}):
        self.logger = logging.getLogger('quads.ServerTech')
        self.prompt = "Switched CDU: "
        self.session = Connect.Connect(host,user,password,options)
        self.plugs = {}
        self.powerstrips = {}
        if not self.session.special_login(prompt=self.prompt):
            self.logger.error("Error logging in")
            exit(1)

    """
    """
    def get_outlets(self):
        interfaces = []
        outlets = self.session.execute("status",["More",self.prompt])
        if len(outlets[0]) < 1 :
            return False
        interfaces.append(outlets[0])
        while outlets[1] is 0 :
            outlets = self.session.send("y",["More","Command successful"])
            if outlets[1] is 0 :
                interfaces.append(outlets[0])
            if outlets[1] is 1 :
                interfaces.append(outlets[0])
                break
        for lines in interfaces :
            for line in lines:
                if len(line.strip()) < 3 :
                    continue
                if re.findall(r"\(Y/es|Outlet\s|status|State|control|ID|Name|successful",line):
                    continue
                data = line.strip().split()
                if re.findall(r"^\.[a-zA-Z]",data[0]) :
                    out = Outlets.Outlets(data[0])
                    out.set_name(data[1])
                    out.set_state(data[2])
                    self.plugs[data[0]] = out
        return self.plugs

    """
    """
    def powerstrip_usage(self) :
        interfaces = []
        strips = self.session.execute("istat",[self.prompt])
        if len(strips[0]) > 0 :
            interfaces.append(strips[0])
        for lines in interfaces :
            for line in lines:
                if len(line.strip()) < 3 :
                    continue
                if re.findall(r"\(Y/es|istat|Input|Load|Power|Voltage|status|State|control|ID|Name|successful",line):
                    continue
                values = line.strip().split()
                if re.findall(r"^\.[a-zA-Z]",values[0]) :
                    out = PowerStrip.PowerStrip(values[0])
                    out.set_name(values[1])
                    out.set_state(values[3],values[4],values[5])
                    self.powerstrips[values[0]] = out
        return self.powerstrips

    ""
    ""
    def get_powerstrip_usage(self):
        if len(self.powerstrips) > 0 :
            for strip in self.powerstrips :
                state = self.powerstrips[strip].get_state()
                self.logger.info("{} : {} volts, {} amps, {} watts".format(strip,state[0],state[1],state[2]))

    """
    """
    def state(self,uuid):
        if len(self.plugs) < 1 :
            self.get_outlets()
        if uuid in self.plugs :
            return self.plugs[uuid].get_state()
        else :
            self.logger.error("Outlet not found.")
            exit(1)

    """
    """
    def on(self,uuid):
        check_state = 3
        if self.plugs < 1 :
            self.get_outlets()
        if self.plugs[uuid].get_state() == "on":
            return True
        else:
            on = self.session.execute("on {}".format(uuid),self.prompt)
            self.get_outlets()
            if self.state(uuid) == "on" :
                return True

    """
    """
    def off(self,uuid):
        check_state = 3
        if self.plugs < 1 :
            self.get_outlets()
        if self.plugs[uuid].get_state() == "off":
            return True
        else:
           off = self.session.execute("off {}".format(uuid),self.prompt)
           self.get_outlets()
           if self.state(uuid) == "off" :
               return True

    """
    """
    def drain(self,uuid):
        self.off(uuid)
        time.sleep(30)
        self.on(uuid)
