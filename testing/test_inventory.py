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

@pytest.fixture(scope='function', autouse=True)
def quads_init():
    args = Test_Inventory.quads + " --init --force"
    sp.call(args, shell=True)

    args = Test_Inventory.quads + " --define-cloud cloud01 --description cloud01"
    sp.call(args, shell=True)

    args = Test_Inventory.quads + " --define-cloud cloud02 --description cloud02"
    sp.call(args, shell=True)

    args = Test_Inventory.quads + " --define-host host01 --default-cloud cloud02"	
    sp.call(args, shell=True) == 1	

@pytest.fixture(scope='function')
def quads_config():
    pass

class Test_Inventory:
    quads = "../bin/quads.py"
   
    def test_quads_init_fail(self):
       
        args = Test_Inventory.quads + " --init"
        assert sp.call(args, shell=True) == 1

    def test_quads_init_pass(self):
       
        args = Test_Inventory.quads + " --init --force"
        assert sp.call(args, shell=True) == 0

    def test_update_clouds_pass(self):
        
        args = Test_Inventory.quads + " --define-cloud cloud03 --description cloud03"
        assert sp.call(args, shell=True) == 0
   
    def test_update_clouds_fail(self):
        
        args = Test_Inventory.quads + " --define-cloud cloud01 --description cloud01"
        assert sp.call(args, shell=True) == 1
       
    def test_update_hosts_pass(self):
       
        args = Test_Inventory.quads + " --define-host host05 --default-cloud cloud01"
        assert sp.call(args, shell=True) == 0

    def test_update_hosts_fail(self):
       
        args = Test_Inventory.quads + " --define-host host01 --default-cloud cloud02"	
        assert sp.call(args, shell=True) == 1      
       
    def test_remove_host_pass(self):
       
        args = Test_Inventory.quads + " --rm-host host01"
        assert sp.call(args, shell=True) == 0

    def test_remove_host_fail(self):
       
        args = Test_Inventory.quads + " --rm-host host10"
        assert sp.call(args, shell=True) == 1
       
    def test_remove_cloud_pass(self):
       
        args = Test_Inventory.quads + " --rm-cloud cloud01"
        assert sp.call(args, shell=True) == 0

    def test_remove_cloud_fail(self):
       
        args = Test_Inventory.quads + " --rm-cloud cloud10"
        assert sp.check_output(args, shell=True) == 'cloud10 not found\n'

    def test_list_hosts_pass(self):

	args = Test_Inventory.quads + " --define-host host01 --default-cloud cloud01"
        sp.call(args, shell=True)
       
        args = Test_Inventory.quads + " --ls-hosts"
        assert sp.check_output(args, shell=True) == "host01\n"
       
    def test_list_hosts_fail(self):
       
        args = Test_Inventory.quads + " --ls-hosts"
	with pytest.raises(AssertionError):
            assert sp.check_output(args, shell=True) == "listing"
       
    def test_list_clouds_pass(self):
       
        args = Test_Inventory.quads + " --ls-clouds"
        assert sp.check_output(args, shell=True) == "cloud01\ncloud02\n"

    def test_list_clouds_fail(self):
       
        args = Test_Inventory.quads + " --ls-clouds"
	with pytest.raises(AssertionError):
            assert sp.check_output(args, shell=True) == "cloud02\n"

           
    def test_write_data(self):
       
        pass
       
    def test_sync_state(self):
       
        pass
