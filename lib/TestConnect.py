import Apc
import ServerTech
import PowerManagement
import Outlets
import pprint
import time
import logging
import sys
import inspect

def main() :
    logger = logging.getLogger('quads')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.info("PowerStrip Work")

    # Old ass SSH crap
#    options = {
#            "KexAlgorithms": "+diffie-hellman-group1-sha1",
#            "HostKeyAlgorithms": "+ssh-dss",
#            "StrictHostKeyChecking": "no",
#            "UserKnownHostsFile": "/dev/null"}

#    logger.info("Connecting to ServerTech")
#    s = ServerTech.ServerTech(user="admn",
#                          password="admn",
#                          host="",
#                          options=options)

#    logger.info("Current state of BC7 : {}".format(s.state(".BC7")))
#    logger.info("Turning off BC7")
#    s.off(".BC7")
#    logger.info("Current state of BC7 : {}".format(s.state(".BC7")))
#    logger.info("Turning on BC7")
#    s.on(".BC7")
#    logger.info("Current state of BC7 : {}".format(s.state(".BC7")))
#    s.powerstrip_usage()
#    s.get_powerstrip_usage()

#    options = {
#            "StrictHostKeyChecking": "no",
#            "UserKnownHostsFile": "/dev/null"}

#    logger.info("Connecting to APC")
#    a = Apc.Apc(user="apc",
#                password="apc",
#                host="",
#                options=options)

#    logger.info("Current state of 18 : {}".format(a.state("18")))
#    logger.info("Turning off 18")
#    a.off("18")
#    logger.info("Current state of 18 : {}".format(a.state("18")))
#    logger.info("Turning on 18")
#    a.on("18")
#    logger.info("Current state of 18 : {}".format(a.state("18")))
    #print a.powerstrip_usage()


if __name__ == '__main__':
    sys.exit(main())
