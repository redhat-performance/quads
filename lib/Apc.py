import PowerManagement
import Outlets
import PowerStrip
import Connect
import time
import re
import logging

class Apc(PowerManagement.PowerManagement):

    def __init__(self,user,password,host,options={}):
        self.logger = logging.getLogger('quads.apc')
        self.prompt = "apc\>"
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
        outlets = self.session.execute("olStatus all",self.prompt)
        if len(outlets[0]) < 1 :
            return False
        for line in outlets[0]:
                if len(line.strip()) < 3 :
                    continue
                if re.findall(r"Success|Status",line):
                    continue
                data = line.strip().split(':')
                out = Outlets.Outlets(data[0])
                out.set_name(data[1])
                out.set_state(data[2])
                self.plugs[data[0]] = out
        return self.plugs

    """
    """
    def powerstrip_usage(self) :
        interfaces = []
        strips_watts = self.session.execute("phReading all power",self.prompt)
        strips_amps = self.session.execute("phReading all current",self.prompt)
        strips_volts = self.session.execute("phReading all voltage",self.prompt)
        data = {}
        if len(strips_volts[0]) > 0 and len(strips_amps[0]) > 0 and len(strips_watts[0] > 0 ):
            for line in strip_volts:
                if len(line.strip()) < 3 :
                    continue
                if re.findall(r"Success|voltage",line):
                    continue
                values = line.strip().split()
                data[values[0]] = {'volts':values[1]}
            for line in strip_amps:
                if len(line.strip()) < 3 :
                    continue
                if re.findall(r"Success|amps",line):
                    continue
                values = line.strip().split()
                data[values[0]] = {'amps':values[1]}
            for line in strip_watts:
                if len(line.strip()) < 3 :
                    continue
                if re.findall(r"Success|power",line):
                    continue
                values = line.strip().split()
                data[values[0]] = {'watts':values[1]}

        #out = PowerStrip.PowerStrip(values[0])
        #out.set_state(values[3],values[4],values[5])
        #self.powerstrips[values[0]] = out
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
            on = self.session.execute("olOn {}".format(uuid),self.prompt)
            self.get_outlets()
            if self.state(uuid) == "on" :
                return True
            else:
                return False

    """
    """
    def off(self,uuid):
        check_state = 3
        if self.plugs < 1 :
            self.get_outlets()
        if self.plugs[uuid].get_state() == "off":
            return True
        else:
           off = self.session.execute("olOff {}".format(uuid),self.prompt)
           self.get_outlets()
           if self.state(uuid) == "off" :
               return True
           else:
               return False

    """
    """
    def drain(self,uuid):
        self.off(uuid)
        time.sleep(30)
        self.on(uuid)
