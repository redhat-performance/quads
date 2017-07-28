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

import pexpect
import logging
import time
import sys

class Connect(object):
    def __init__(self,host,user,password,options={}):
        self.logger = logging.getLogger('Strip.Connect')
        self.user = user
        self.host = host
        self.password = password
        self.session = None
        self.prompt = None
        self.options = options

    def special_login(self,prompt=None):
        if prompt :
            self.prompt = prompt
        extra = ""
        for option in self.options :
            extra = "{} -o \"{}={}\" ".format(extra,option,self.options[option])
        self.session = pexpect.spawn("ssh {} {}@{}".format(extra,self.user,self.host),timeout=60)
        self.session.delaybeforesend = None
        #self.session.logfile = sys.stdout
        login = self.session.expect('[Pp]assword: ')
        if login == 0:
            self.logger.info("Logging in: {}".format(self.host))
            self.session.sendline(self.password)
            success = self.session.expect(self.prompt)
            if success == 0 :
                return True
            else:
                return False

    def login(self,prompt=None):
        try:
            self.session = pxssh.pxssh(options=self.options)
            if prompt :
                self.session.login(self.host,
                                   self.user,
                                   self.password,
                                   auto_prompt_reset=False)
                self.session.PROMPT = prompt
            else:
                self.session.login(self.host,self.user,self.password)
        except pxssh.ExceptionPxssh as e:
            self.logger.error("Exception : {}".format(e))
            return False
        return True

    def send(self, command, expect=None):
        self.logger.debug("Sending : {}".format(command))
        self.session.send(command)
        pos = self.session.expect(expect)
        lines = self.session.before.split("\r\n")
        return lines, pos

    def execute(self, command, expect=None):
        self.logger.debug("Executing: {}".format(command))
        self.session.sendline(command)
        time.sleep(5)
        pos = self.session.expect(expect)
        lines = self.session.before.split("\r\n")
        return lines, pos
