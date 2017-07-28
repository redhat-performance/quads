import pexpect
import logging
import time
import sys

class Connect(object):
    def __init__(self,host,user,password,options={}):
        self.logger = logging.getLogger("Connect")
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
        self.session.logfile = sys.stdout
        login = self.session.expect('Password: ')
        if login == 0:
            print "Logging in"
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
            print e
            return False
        return True

    def send(self, command, expect=None):
        print "Sending : {}".format(command)
        self.session.send(command)
        time.sleep(15)
        pos = self.session.expect(expect)
        lines = self.session.before.split("\r\n")
        return lines, pos

    def execute(self, command, expect=None):
        print "Executing: {}".format(command)
        self.session.sendline(command)
        time.sleep(15)
        pos = self.session.expect(expect)
        lines = self.session.before.split("\r\n")
        return lines, pos
