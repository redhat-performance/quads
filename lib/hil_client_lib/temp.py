"""This module sets up a HIL client"""
import os
import sys
import requests
import yaml

sys.path.append(os.path.dirname(__file__) + "/../../bin")
#for i in sys.path:
#    print i


print __file__ 
dir = os.path.dirname(__file__)
print 'dirname:'+ dir

print os.path.dirname(os.path.abspath(__file__))
