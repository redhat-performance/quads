import PowerManagement
import Outlets
import Connect
import time
import re
import pprint

class ServerTech(PowerManagement.PowerManagement):

    def __init__(self,user,password,host,options={}):
        self.prompt = "Switched CDU: "
        self.session = Connect.Connect(host,user,password,options)
        self.plugs = {}
        if not self.session.special_login(prompt=self.prompt):
            print "Error logging in"
            exit(1)

    def get_outlets(self):
        interfaces = []
        outlets = self.session.execute("status",["More",self.prompt])
        if len(outlets[0]) > 0 :
            interfaces.append(outlets[0])
        while outlets[1] is 0 :
            time.sleep(2)
            outlets = self.session.execute("y",["More",self.prompt])
            interfaces.append(outlets[0])
        for lines in interfaces :
            for line in lines:
                if len(line.strip()) < 3 :
                    continue
                if re.findall(r"\(Y/es|Outlet\s|status|State|control|ID|Name|successful",line):
                    continue
                data = line.strip().split("    ")
                out = Outlets.Outlets(data[0])
                out.set_name(data[1])
                out.set_state(data[2])
                self.plugs[data[0]] = out
        return self.plugs

    def strip_power(self) :
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

    def state(self,uuid):
        if len(self.plugs) < 1 :
            self.get_outlets()
        if self.plugs[uuid] :
            return self.plugs[uuid].get_state()
        else :
            print "Outlet not found."
            exit(1)

    def on(self):
        pass

    def off(self):
        pass

    def reset(self):
        pass

    def drain(self):
        pass
