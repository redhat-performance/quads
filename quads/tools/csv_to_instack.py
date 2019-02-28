#!/usr/bin/env python

# This code was shamelessly plucked out of another
# repo.  Originally written by Joe Talerico <jtaleric at redhat dot com>

import argparse
import csv
import json
import logging
import sys
from collections import defaultdict

logger = logging.getLogger(__name__)


def csv_to_instack(input_file):

    with open(input_file, 'r') as csvFile:
        data = list(csv.reader(csvFile))

    json_data = defaultdict(list)
    for value in data[1:]:
        json_data['nodes'].append({
            'pm_password': value[3],
            'pm_type': value[4],
            'mac': [value[0]],
            'cpu': "2",
            'memory': "1024",
            'disk': "20",
            'arch': "x86_64",
            'pm_user': value[2],
            'pm_addr': value[1]})

    return json.dumps(json_data, indent=4, sort_keys=True)


def main():
    parser = argparse.ArgumentParser(description="CSV to instack converter")
    parser.add_argument(
        '-c', '--csv',
        dest='inputfile',
        help='Path to CSV file to convert',
        default=None,
        type=str,
        required=True
    )

    args = parser.parse_args()
    input_file = args.inputfile

    instack_env = csv_to_instack(input_file)
    logger.info(instack_env)
    return 0


if __name__ == "__main__":
    sys.exit(main())
