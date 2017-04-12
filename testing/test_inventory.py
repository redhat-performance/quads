#!/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 10:53:15 2017

@author: djfinn14
"""

import pytest
import yaml
import argparse
import os
import sys
import subprocess as sp

sys.path.append(os.path.dirname(__file__) + "/../lib")
sys.path.append(os.path.dirname(__file__) + "/../lib/hardware_services/inventory_drivers/")
sys.path.append(os.path.dirname(__file__) + "/../lib/hardware_services/")
import libquads

@pytest.fixture(scope="function")
def quads_setup():
    libquads.Quads("","","","","","","","")
   # args = Test_Inventory.quads + " --init --force"
  #  sp.call(args, shell=True)

@pytest.fixture
def quads_config():
    pass

@pytest.mark.userfixed("quads_setup")
class Test_Inventory:
    quads = "../bin/quads.py"
    
    def test_quads_init_fail(self):
        pass
        inventoryservice = "Mock"
        libquads.Quads("","","","","","","",inventoryservice) == 1
    #    args = Test_Inventory.quads + " --init"
     #   assert sp.call(args, shell=True) == 1

    def test_quads_init_pass(self):
        pass
      #  args = Test_Inventory.quads + " --init --force"
       # assert sp.call(args, shell=True) == 0
    
    def test_update_clouds(self):
        pass
       # quads_init()
        
       # args = Test_Inventory.quads + " --define-cloud cloud01 --description cloud01"
       # assert sp.call(args, shell=True) == 0
        
    def test_update_hosts_pass(self):
        pass
      #  quads_init()
        
      #  args = Test_Inventory.quads + " --define-cloud host01 --default-cloud cloud01"
      #  assert sp.call(args, shell=True) == 0
        
        
    def test_write_data(self):
        
        pass
        
    def test_sync_state(self):
        
        pass
        
        
    def test_remove_host(self):
        pass
      #  quads_init()
        
      #  args = Test_Inventory.quads + " --rm-host host01"
      #  sp.call(args, shell=True)
        
    def test_remove_cloud(self):
        pass
      #  quads_init()
        
      #  args = Test_Inventory.quads + " --rm-cloud cloud01"
      #  sp.call(args, shell=True)
        
    def test_list_hosts(self):
        pass
      #  quads_init()
        
      #  args = Test_Inventory.quads + " --ls-hosts"
      #  sp.call(args, shell=True)
        
    def test_list_clouds(self):
        pass
      #  quads_init()
        
      #  args = Test_Inventory.quads + " --ls-clouds"
      #  sp.call(args, shell=True)
    