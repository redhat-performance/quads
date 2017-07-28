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
import pexpect
import Connect
import time
import re
import logging

class Apc(PowerManagement.PowerManagement):

    def __init__(self,user,password,host,options={}):
        if len(options) < 1 :
            options = {"StrictHostKeyChecking": "no",
                       "UserKnownHostsFile": "/dev/null"}
        self.logger = logging.getLogger('Strip.apc')
        self.prompt = "apc\\>"
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
                out.name = data[1]
                out.state = data[2]
                self.plugs[data[0]] = out
        return self.plugs

    """
    TODO : APC is not responding well to querying the usage.
    """
    def powerstrip_usage(self) :
        interfaces = []
        expect = [self.prompt,pexpect.EOF]
        strips_watts = self.session.execute("phReading all power",expect)
        strips_amps = self.session.execute("phReading all current",expect)
        # This line breaks me...
        strips_volts = self.session.execute("phReading all voltage",expect)
        data = {}
        if len(strips_volts) > 0 and len(strips_amps) > 0 and len(strips_watts) > 0 :
            for line in strips_volts[0]:
                if len(line.strip()) < 3 :
                    continue
                if re.findall(r"Success|voltage",line):
                    continue
                values = line.strip().split()
                data[values[0]] = {'volts':values[1]}
            for line in strips_amps[0]:
                if len(line.strip()) < 3 :
                    continue
                if re.findall(r"Success|amps",line):
                    continue
                values = line.strip().split()
                data[values[0]] = {'amps':values[1]}
            for line in strips_watts[0]:
                if len(line.strip()) < 3 :
                    continue
                if re.findall(r"Success|power",line):
                    continue
                values = line.strip().split()
                data[values[0]] = {'watts':values[1]}

        return self.powerstrips

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
            on = self.session.execute("olOn {}".format(uuid),self.prompt)
            self.outlets()
            if self.state(uuid) == "on" :
                return True
            else:
                return False

    """
    """
    def off(self,uuid):
        check_state = 3
        if self.plugs < 1 :
            self.outlets()
        if self.plugs[uuid].state == "off":
            return True
        else:
           off = self.session.execute("olOff {}".format(uuid),self.prompt)
           self.outlets()
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
