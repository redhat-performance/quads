#!/bin/python

import itertools
import string
import argparse
import os
import sys
import array
from subprocess import call
from subprocess import check_call

parser = argparse.ArgumentParser(description='Print subsets of lines from an input file')
parser.add_argument('-i', '--input', dest='inputfile',
                                            help='Input file containing lines of input',
                                            default=None, type=str)
parser.add_argument('--count', dest='count', type=int, default=None, help='number of lines in subset')

def printf(format, *args):
    sys.stdout.write(format % args)

args = parser.parse_args()
inputfile = args.inputfile
count = args.count

lines = []
if inputfile is not None:
	if os.path.exists(inputfile):
		try:
			with open(inputfile) as f:
				lines = f.readlines()
		except Exception, ex:
			print ex
			exit(1)

i = []
for j in range(0, len(lines)):
    i.append(j)

if count <= len(lines):
    combos = list(itertools.combinations(i, count))
else:
    exit(1)

for k in range(0, len(combos)):
    reset = 0
    for n in combos[k]:
        if reset < count - 1:
            printf("%s,", lines[n].rstrip('\n'))
        else:
            printf("%s", lines[n].rstrip('\n'))
        reset = reset + 1
    printf('\n')
