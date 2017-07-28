import ServerTech
import pprint

# Old ass SSH crap
options = {
            "KexAlgorithms": "+diffie-hellman-group1-sha1",
            "HostKeyAlgorithms": "+ssh-dss",
            "StrictHostKeyChecking": "no",
            "UserKnownHostsFile": "/dev/null"}

s = ServerTech.ServerTech(user="admn",
                          password="admn",
                          host="my_strip",
                          options=options)
print s.state(".BC7")
#print s.strip_power()
