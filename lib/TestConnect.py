import ServerTech
import pprint
import time

# Old ass SSH crap
options = {
            "KexAlgorithms": "+diffie-hellman-group1-sha1",
            "HostKeyAlgorithms": "+ssh-dss",
            "StrictHostKeyChecking": "no",
            "UserKnownHostsFile": "/dev/null"}

s = ServerTech.ServerTech(user="admn",
                          password="admn",
                          host="",
                          options=options)
print s.state(".BC7")
s.off(".BC7")
print s.state(".BC7")
s.on(".BC7")
print s.state(".BC7")
