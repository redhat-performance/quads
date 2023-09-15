#!/usr/bin/env python3

import os
import json

from jsonpath_ng import parse

from quads.server.dao.disk import DiskDao
from quads.server.dao.host import HostDao
from quads.server.dao.memory import MemoryDao
from quads.server.dao.processor import ProcessorDao

MD_DIR = "/var/www/html/lshw"
DISK_TYPES = {"nvme": "nvm", "sata": "ata", "scsi": "scsi"}


def b2g(num, metric=False):
    factor = 1024
    if metric:
        factor = 1000
    return round(num / (factor**3))


for _d, _, _files in os.walk(MD_DIR):
    for _file in _files:
        filename = os.path.join(MD_DIR, _file)
        if os.path.getsize(filename):
            path, extension = os.path.splitext(filename)
            if extension == ".json":
                with open(filename) as _f:
                    data = json.load(_f)
                    children = parse("$..children[*]").find(data)
                    hostname = parse("$.id").find(data)[0].value
                    host_obj = HostDao.get_host(hostname)
                    if not host_obj:
                        print(f"Host not found: {hostname}")
                        break
                    # interfaces
                    for child in [
                        child for child in children if child.value["class"] == "network"
                    ]:
                        if child.value.get("vendor"):
                            for host_interface in host_obj.interfaces:
                                if host_interface.mac_address == child.value["serial"]:
                                    host_interface.vendor = child.value.get("vendor")
                                    host_interface.logical_name = child.value.get(
                                        "logicalname"
                                    )
                                    speed = child.value["configuration"].get("speed")
                                    if speed:
                                        speed = int("".join(filter(str.isdigit, speed)))
                                    host_interface.speed = speed
                                    host_obj.save()
                    # disks
                    for child in [
                        child for child in children if child.value["class"] == "disk"
                    ]:
                        if child.value.get("size"):
                            disk_type = None
                            for dt, sub in DISK_TYPES.items():
                                if child.value["description"].lower().startswith(sub):
                                    disk_type = dt
                            disk_size = b2g(int(child.value["size"]), True)
                            filters = {
                                "name": host_obj.name,
                                "disks__disk_type": disk_type,
                                "disks__size_gb": disk_size,
                            }
                            host = HostDao.filter_hosts_dict(filters)
                            if host:
                                for disk in host[0].disks:
                                    if disk.disk_type == disk_type and disk.disk_size == disk_size:
                                        disk.count += 1
                            else:
                                disk = DiskDao.create_disk(hostname=host_obj.name, disk_type=disk_type,
                                                           size_gb=disk_size, count=1)

                    # memory
                    for memory in host_obj.memory:
                        MemoryDao.delete_memory(memory.id)
                    for child in [
                        child
                        for child in children
                        if child.value["class"] == "memory"
                        and "bank" not in child.value["id"]
                    ]:
                        if (
                            child.value.get("size")
                            and child.value.get("handle")
                            and "cache" not in child.value["id"]
                        ):
                            MemoryDao.create_memory(
                                hostname,
                                handle=child.value.get("handle"),
                                size_gb=b2g(int(child.value["size"])),
                            )

                    # processor
                    for processor in host_obj.processors:
                        ProcessorDao.delete_processor(processor.id)
                    for child in [
                        child
                        for child in children
                        if child.value["class"] == "processor"
                    ]:
                        configuration = child.value.get("configuration")
                        processor = ProcessorDao.create_processor(
                            hostname,
                            handle=child.value.get("handle"),
                            vendor=child.value.get("vendor"),
                            product=child.value.get("product"),
                            cores=int(configuration.get("cores", 0)),
                            threads=int(configuration.get("threads", 0)),
                        )
