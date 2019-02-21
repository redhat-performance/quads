#! /usr/bin/env python

import os

from datetime import datetime

from helpers import is_supported
from quads.model import Host
from quads.tools.badfish import Badfish
from quads.tools.foreman import Foreman
from quads.config import conf


def reconfigure(_host, _idrac_host):
    interfaces = os.path.dirname(__file__) + "/../../conf/idrac_interfaces.yml"

    if is_supported(_host.name):
        badfish = Badfish(_idrac_host, conf["ipmi_username"], conf["ipmi_password"])

        host_type = "foreman"
        if _host.nullos:
            host_type = "director"

        try:
            badfish.change_boot(host_type, interfaces, True)
        except SystemExit:
            print("Something went wrong.")
            return
        _host.update(build=False, realeased=True, last_build=datetime.now())
        return
    else:
        _host.update(build=False, realeased=True, last_build=datetime.now())
        return


if __name__ == "__main__":
    foreman = Foreman(
        conf["foreman_api_url"],
        conf["foreman_username"],
        conf["foreman_password"]
    )

    # get all overcloud hosts
    overclouds = foreman.get_parametrized("params.%s" % conf["foreman_director_parameter"], "true")
    for host in overclouds:
        _quads_host = Host.objects(name=host).first()
        if _quads_host and not _quads_host.nullos:
            build_state = foreman.get_host_build_status(host)
            if build_state:
                _quads_host.update(nullos=True, build=True)

    # get all undercloud hosts
    underclouds = foreman.get_parametrized("params.%s" % conf["foreman_director_parameter"], "false")
    for host in underclouds:
        _quads_host = Host.objects(name=host).first()
        if _quads_host and _quads_host.nullos:
            _quads_host.update(nullos=False, build=True)

    hosts = Host.objects(build=True).all()
    for host in hosts:
        idrac_host = foreman.get_idrac_host(host.name)
        reconfigure(host, idrac_host)
