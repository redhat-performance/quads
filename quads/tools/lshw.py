import os

from quads.server.dao.cloud import CloudDao
from quads.server.dao.host import HostDao
from quads.tools.ssh_helper import SSHHelper

LSHW_OUTPUT_DIR = "/var/www/html/lshw/"


def run_lshw(hostname: str, file_path: str) -> None:
    """
    Connect via SSHHElper with the remote host and run lshw command
    :param hostname: the remote host FQDN
    :param file_path: the full file path were the output of lshw is stored
    :return: None
    """
    try:
        ssh_helper = SSHHelper(hostname)
    except Exception:
        print(f"Something went wrong trying to connect to: {hostname}")
        return
    _, output = ssh_helper.run_cmd("lshw -xml")
    if output:
        with open(file_path, "w") as _file:
            for line in output:
                _file.writelines(line)


def main() -> None:
    """
    Main function
    :return: None
    """
    cloud = CloudDao.get_cloud("cloud01")
    hosts = HostDao.filter_hosts(cloud=cloud, retired=False, broken=False)
    for host in hosts:
        file_name = f"{host.name}.xml"
        file_path = os.path.join(LSHW_OUTPUT_DIR, file_name)
        if os.path.exists(file_path):
            if os.path.getsize(file_path) < 1:
                run_lshw(host.name, file_path)
        else:
            run_lshw(host.name, file_path)


if __name__ == "__main__":
    main()
