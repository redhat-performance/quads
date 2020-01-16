#!/usr/bin/python3

import logging
import os
import socket

from ssh2.session import Session

logger = logging.getLogger(__name__)
logging.getLogger("libssh2").setLevel(logging.WARNING)


class SSHHelper(object):
    def __init__(self, _host, _user="root", _password=None, _public_key=None):
        self.host = _host
        self.user = _user
        self.password = _password
        self.public_key = _public_key
        self.sock = None
        self.session = None
        self.channel = self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, 22))

        self.session = Session()
        self.session.handshake(self.sock)
        if self.password:
            self.session.userauth_password(self.user, self.password)
        elif self.public_key:
            self.session.userauth_publickey_fromfile(
                self.user,
                os.path.splitext(self.public_key)[0],
                "",
                self.public_key
            )
        else:
            self.session.agent_auth(self.user)

        self.session.set_blocking(True)

        channel = self.session.open_session()
        return channel

    def disconnect(self):
        self.channel.close()
        self.session.disconnect()
        self.sock.close()

    def run_cmd(self, cmd):
        lines = []
        self.channel.execute(cmd)
        size, data = self.channel.read()
        while size:
            logger.debug(data)
            lines.append(data)
            size, data = self.channel.read()
        status = self.channel.get_exit_status()
        if status != 0:
            logger.error(f"There was something wrong with your request: {status}")
            return False
        else:
            logger.debug("Command executed successfully: %s" % cmd)
            return "".join([line.decode(encoding="utf-8") for line in lines])

    def copy_ssh_key(self, _ssh_key):

        with open(_ssh_key, "r") as _file:
            key = _file.readline().strip()

        command = 'echo "%s" >> ~/.ssh/authorized_keys' % key
        self.run_cmd(command)
