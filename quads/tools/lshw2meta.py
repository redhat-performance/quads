#!/usr/bin/env python3

import os
import json

from typing import List, Union
from jsonpath_ng import parse
from quads.model import Host, Processor, Memory, Interface, Disk

MD_DIR = '/var/www/html/lshw'


METRIC_LABELS: List[str] = ["B", "kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
BINARY_LABELS: List[str] = ["B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"]
PRECISION_OFFSETS: List[float] = [0.5, 0.05, 0.005, 0.0005]  # PREDEFINED FOR SPEED.
PRECISION_FORMATS: List[str] = ["{}{:.0f} {}", "{}{:.1f} {}", "{}{:.2f} {}", "{}{:.3f} {}"]  # PREDEFINED FOR SPEED.
DISK_TYPES = {"nvme": "nvm", "sata": "ata", "scsi": "scsi"}


def format(num: Union[int, float], metric: bool = False, precision: int = 1, index: int = None) -> str:
    # TODO: convert only to GB
    """
    Human-readable formatting of bytes, using binary (powers of 1024)
    or metric (powers of 1000) representation.
    """

    assert isinstance(num, (int, float)), "num must be an int or float"
    assert isinstance(metric, bool), "metric must be a bool"
    assert isinstance(precision, int) and 0 <= precision <= 3, "precision must be an int (range 0-3)"

    unit_labels = METRIC_LABELS if metric else BINARY_LABELS
    last_label = unit_labels[-1]
    unit_step = 1000 if metric else 1024
    unit_step_thresh = unit_step - PRECISION_OFFSETS[precision]

    is_negative = num < 0
    if is_negative:  # Faster than ternary assignment or always running abs().
        num = abs(num)

    for i, unit in enumerate(unit_labels):
        if index:
            num /= unit_step
            if i == index:
                break
        else:
            if num < unit_step_thresh:
                break
            if unit != last_label:
                num /= unit_step

    return PRECISION_FORMATS[precision].format("-" if is_negative else "", round(num), unit)


for _d, _, _files in os.walk(MD_DIR):
    for _file in _files:
        filename = os.path.join(MD_DIR, _file)
        if os.path.getsize(filename):
            path, extension = os.path.splitext(filename)
            if extension == ".json":
                with open(filename) as _f:
                    data = json.load(_f)
                    childs = parse('$..children[*]').find(data)
                    hostname = parse('$.id').find(data)[0].value
                    host_obj = Host.objects(name=hostname).first()
                    if not host_obj:
                        print(f"Host not found: {hostname}")
                        break
                    for child in [child for child in childs if child.value["class"] == "network"]:
                        if child.value.get('vendor'):
                            for host_interface in host_obj.interfaces:
                                if host_interface.mac_address == child.value["serial"]:
                                    host_interface.vendor = child.value.get('vendor')
                                    host_interface.logical_name = child.value.get('logicalname')
                                    # TODO: convert speed to int
                                    host_interface.speed = child.value.get('speed')
                                    Host.objects(
                                        name=hostname, interfaces__mac_address=child.value['serial']
                                    ).update_one(set_interfaces__S=host_interface)
                    for child in [child for child in childs if child.value["class"] == "disk"]:
                        if child.value.get('size'):
                            disk_type = None
                            for dt, sub in DISK_TYPES.items():
                                if child.value["description"].lower().startswith(sub):
                                    disk_type = dt
                            disk = Disk(
                                disk_type=disk_type,
                                logical_name=child.value['logicalname'],
                                size_gb=format(int(child.value['size']), True)
                            )
                            updated = Host.objects(
                                host__disks__logical_name=child.value['logicalname']
                            ).update_one(set__disks__S=disk)
                            if not updated:
                                Host.objects.update_one(push__disks=disk)
                    for child in [child for child in childs if child.value["class"] == "memory" and "bank" not in child.value["id"]]:
                        if child.value.get("size") and child.value.get("handle") and "cache" not in child.value["id"]:
                            memory = Memory(
                                handle=child.value.get('handle'),
                                size_gb=format(int(child.value['size']))
                            )
                            updated = Host.objects(
                                host__memory__handle=child.value.get('handle')
                            ).update_one(set__memory__S=memory)
                            if not updated:
                                Host.objects.update_one(push__memory=memory)
                    for child in [child for child in childs if child.value["class"] == "processor"]:
                        processor = Processor(
                            handle=child.value.get('handle'),
                            vendor=child.value.get('vendor'),
                            product=child.value.get('product'),
                            core=child.value.get('core'),
                            threads=child.value.get('threads'),
                        )
                        updated = Host.objects(
                            host__processors__handle=child.value.get('handle')
                        ).update_one(set__processors__S=processor)
                        if not updated:
                            Host.objects.update_one(push__processors=processor)
