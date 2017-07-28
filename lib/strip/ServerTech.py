#   Copyright 2017 Joe Talerico
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import PowerManagement
import Outlets
import PowerStrip
import Connect
import time
import re
import logging

class ServerTech(PowerManagement.PowerManagement):

    def __init__(self,user,password,host,options={}):
        if len(options) < 1 :
            options = {
                    "KexAlgorithms": "+diffie-hellman-group1-sha1",
                    "HostKeyAlgorithms": "+ssh-dss",
                    "StrictHostKeyChecking": "no",
                    "UserKnownHostsFile": "/dev/null"}
        self.logger = logging.getLogger('Strip.ServerTech')
        self.prompt = "Switched CDU: "
        self.session = Connect.Connect(host,user,password,options)
        self.plugs = {}
        self.powerstrips = {}
        if not self.session.special_login(prompt=self.prompt):
            self.logger.error("Error logging in")
            exit(1)

    """
    """
    def outlets(self):
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
                    out.name = data[1]
                    out.state = data[2]
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
                    out.name = values[1]
                    out.volts = values[3]
                    out.amps = values[4]
                    out.wattage = values[5]
                    self.powerstrips[values[0]] = out

    ""
    ""
    def usage(self):
        self.powerstrip_usage()
        if len(self.powerstrips) > 0 :
            for strip in self.powerstrips :
                watt = self.powerstrips[strip].wattage
                amps = self.powerstrips[strip].amps
                volts = self.powerstrips[strip].volts
                self.logger.info("{} : {} volts, {} amps, {} watts".format(strip,volts,amps,watt))

    """
    """
    def state(self,uuid):
        if len(self.plugs) < 1 :
            self.outlets()
        if uuid in self.plugs :
            return self.plugs[uuid].state
        else :
            self.logger.error("Outlet not found.")
            exit(1)

    """
    """
    def on(self,uuid):
        check_state = 3
        if self.plugs < 1 :
            self.outlets()
        if self.plugs[uuid].state == "on":
            return True
        else:
            on = self.session.execute("on {}".format(uuid),self.prompt)
            self.outlets()
            if self.state(uuid) == "on" :
                return True

    """
    """
    def off(self,uuid):
        check_state = 3
        if self.plugs < 1 :
            self.outlets()
        if self.plugs[uuid].state == "off":
            return True
        else:
           off = self.session.execute("off {}".format(uuid),self.prompt)
           self.outlets()
           if self.state(uuid) == "off" :
               return True

    """
    """
    def drain(self,uuid):
        self.off(uuid)
        time.sleep(30)
        self.on(uuid)
