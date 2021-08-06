#!/usr/bin/env python3

from xml.etree import ElementTree
import os

DIRECTORY = "/var/www/html/lshw/"


def main():
    for _, _, _files in os.walk(DIRECTORY):
        for _file in _files:
            tree = ElementTree.parse(os.path.join(DIRECTORY, _file))
            root = tree.getroot()
            for child in root[0]:
                print(child.tag, child.attrib)


if __name__ == '__main__':
    main()
