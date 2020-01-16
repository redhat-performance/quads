#!/usr/bin/python3

import logging
import os
import socket
from select import select

from ssh2.error_codes import LIBSSH2_ERROR_EAGAIN
from ssh2.session import Session, LIBSSH2_SESSION_BLOCK_INBOUND, LIBSSH2_SESSION_BLOCK_OUTBOUND

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
        self.shell = self.channel.shell()

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

        self.session.set_blocking(False)

        channel = self.session.open_session()

        while channel == LIBSSH2_ERROR_EAGAIN:
            logger.warning("Waiting for socket to be ready")
            self.wait_socket(15)
            channel = self.session.open_session()

        return channel

    def disconnect(self):
        self.session.disconnect()
        self.channel.close()
        self.channel.wait_closed()
        self.sock.close()

    def wait_socket(self, timeout=1):
        """Helper function for testing non-blocking mode.
        This function blocks the calling thread for <timeout> seconds.
        Also available at `ssh2.utils.wait_socket`
        """
        directions = self.session.block_directions()
        if directions == 0:
            return 0
        read_fds = [self.sock] \
            if (directions & LIBSSH2_SESSION_BLOCK_INBOUND) else ()
        write_fds = [self.sock] \
            if (directions & LIBSSH2_SESSION_BLOCK_OUTBOUND) else ()
        return select(read_fds, write_fds, (), timeout)

    def run_cmd(self, cmd):
        lines = []

        while self.channel.execute("%s" % cmd) == LIBSSH2_ERROR_EAGAIN:
            logger.warning("Waiting for socket to be ready")
            self.wait_socket(15)

        self.channel.wait_eof()

        size, data = self.channel.read()

        while size == LIBSSH2_ERROR_EAGAIN:
            logger.warning("Waiting to read data from channel")
            self.wait_socket(15)
            size, data = self.channel.read()

        while size > 0:
            lines.append(data.decode())
            size, data = self.channel.read()

        status = self.channel.get_exit_status()
        if status != 0:
            logger.error(f"There was something wrong with your request: {status}")
            return False
        else:
            logger.debug("Command executed successfully: %s" % cmd)
            return " ".join(lines)

    def copy_ssh_key(self, _ssh_key):

        with open(_ssh_key, "r") as _file:
            key = _file.readline().strip()

        command = 'echo "%s" >> ~/.ssh/authorized_keys' % key
        self.run_cmd(command)
