#!/usr/bin/env python3

import os
import json

from jsonpath_ng import parse
from quads.model import Host, Processor, Memory, Interface, Disk

MD_DIR = '/var/www/html/lshw'
DISK_TYPES = {"nvme": "nvm", "sata": "ata", "scsi": "scsi"}


def b2g(num, metric=False):
    factor = 1024
    if metric:
        factor = 1000
    return round(num/(factor ** 3))


for _d, _, _files in os.walk(MD_DIR):
    for _file in _files:
        filename = os.path.join(MD_DIR, _file)
        if os.path.getsize(filename):
            path, extension = os.path.splitext(filename)
            if extension == ".json":
                with open(filename) as _f:
                    data = json.load(_f)
                    children = parse('$..children[*]').find(data)
                    hostname = parse('$.id').find(data)[0].value
                    host_obj = Host.objects(name=hostname).first()
                    if not host_obj:
                        print(f"Host not found: {hostname}")
                        break
                    # interfaces
                    for child in [child for child in children if child.value["class"] == "network"]:
                        if child.value.get('vendor'):
                            for host_interface in host_obj.interfaces:
                                if host_interface.mac_address == child.value["serial"]:
                                    host_interface.vendor = child.value.get('vendor')
                                    host_interface.logical_name = child.value.get('logicalname')
                                    speed = child.value['configuration'].get('speed')
                                    if speed:
                                        speed = int("".join(filter(str.isdigit, speed)))
                                    host_interface.speed = speed
                                    Host.objects(
                                        name=hostname, interfaces__mac_address=child.value['serial']
                                    ).update_one(set_interfaces__S=host_interface)
                    # disks
                    for child in [child for child in children if child.value["class"] == "disk"]:
                        if child.value.get('size'):
                            disk_type = None
                            for dt, sub in DISK_TYPES.items():
                                if child.value["description"].lower().startswith(sub):
                                    disk_type = dt
                            disk = Disk(
                                disk_type=disk_type,
                                logical_name=child.value['logicalname'],
                                size_gb=b2g(int(child.value['size']), True)
                            )
                            updated = Host.objects(
                                host__disks__logical_name=child.value['logicalname']
                            ).update_one(set__disks__S=disk)
                            if not updated:
                                Host.objects.update_one(push__disks=disk)
                    # memory
                    for child in [child for child in children if child.value["class"] == "memory" and "bank" not in child.value["id"]]:
                        if child.value.get("size") and child.value.get("handle") and "cache" not in child.value["id"]:
                            memory = Memory(
                                handle=child.value.get('handle'),
                                size_gb=b2g(int(child.value['size']))
                            )
                            updated = Host.objects(
                                host__memory__handle=child.value.get('handle')
                            ).update_one(set__memory__S=memory)
                            if not updated:
                                Host.objects.update_one(push__memory=memory)
                    # processor
                    for child in [child for child in children if child.value["class"] == "processor"]:
                        processor = Processor(
                            handle=child.value.get('handle'),
                            vendor=child.value.get('vendor'),
                            product=child.value.get('product'),
                            core=int(child.value.get('core')),
                            threads=int(child.value.get('threads')),
                        )
                        updated = Host.objects(
                            host__processors__handle=child.value.get('handle')
                        ).update_one(set__processors__S=processor)
                        if not updated:
                            Host.objects.update_one(push__processors=processor)
