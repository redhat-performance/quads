#!/usr/bin/env python3
import json
import os

from quads.model import Host

DIRECTORY = "/var/www/html/lshw/"
JSON = "f01-h04-000-1029u.rdu2.scalelab.redhat.com.json"
CLASSES = [
    "bus",
    "memory",
    "processor",
    "bridge",
    "storage",
    "disk",
    "network",
    "volume",
]
VALUES = [
    "id",
    "class",
    "description",
    "vendor",
    "product",
    "logicalname",
    "serial",
    "units",
    "size",
    "capacity",
    "clock",
    "children",
]
network_collection = []
disk_collection = []
processor_collection = []
memory_collection = []


def traverse_children(_childrens):
    collection = []
    for children in _childrens:
        properties = {}
        _class = children.get("class")
        if _class in CLASSES:
            for key in VALUES:
                value = children.get(key)
                if value:
                    properties[key] = value
            _children = properties.get("children")

            if _class == "memory" and not properties.get("size"):
                continue
            if _class == "memory" and properties["id"].startswith("cache"):
                continue
            if _class == "memory" and properties["id"].startswith("firmware"):
                continue
            if _class == "bus" and properties["id"].startswith("usb"):
                continue
            if _class == "bus" and properties["id"].startswith("serial"):
                continue
            if _class == "bus" and properties["id"].startswith("fiber"):
                continue
            if _class == "bridge" and properties["id"].startswith("isa"):
                continue
            if _class == "bridge" and properties["id"].startswith("pci") and not _children:
                continue

            _configuration = properties.get("configuration")
            if _configuration:
                _ip = _configuration.get("ip")
                _speed = _configuration.get("speed")
                if _ip or _speed:
                    properties["configuration"] = {"ip": _ip, "speed": _speed}
            node_children = properties.get("children")
            if node_children:
                if type(node_children) == str:
                    node_children = [node_children]
                node_children = traverse_children(node_children)
                if node_children:
                    properties["children"] = node_children

            if _class == "network":
                network_collection.append(properties)
            if _class == "memory":
                memory_collection.append(properties)
            if _class == "processor":
                processor_collection.append(properties)
            if _class in ["disk", "volume"]:
                disk_collection.append(properties)

            collection.append(properties)
    return collection


def main():
    for root, dirs, files in os.walk(DIRECTORY):
        for _file in files:
            with open(os.path.join(root, _file), "r") as _json:
                data = json.load(_json)
            hostname = data.get("id")
            host = Host.objects(name=hostname).first()
            vendor = data.get("vendor")
            if vendor and not host.vendor:
                host.update(vendor=vendor)
            serial = data.get("serial")
            if serial and not host.serial:
                host.update(serial=serial)
            core = data.get("children")[0]
            core_children = core.get("children")
            results = traverse_children(core_children)
            print(results)
            print(processor_collection)
            print(memory_collection)
            print(disk_collection)
            print(network_collection)


if __name__ == '__main__':
    main()
