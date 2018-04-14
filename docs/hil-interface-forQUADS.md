HIL interface for QUADS
=======================

A step by step guide for interfacing HIL with QUADS.

# PREREQUISITE:
* A HIL server is running and its URL is available.
* QUADS has a non-admin user account in HIL.
* A Project (a.k.a cloud01) is created on HIL which is accessible to the user
* Nodes that will be used by QUADS are already allocated into this project.

# Step 1: Introduce HIL parameters in quads.yml

* These are sample values. Adjust according to your environment. 
```
allocator_activated: true  		# *** Default is 'false') 
allocator_name: HIL 			# Name of the allocator
allocator_url: http://127.0.0.1:6000	# url of HIL server
allocator_pool_name: quads	# Nodes and networks allocated to Quads will reside in project <quads>
allocator_username: quad_user		# QUADS will use this username to log into HIL
allocator_password: quads		# Password of username. 

```
* By default the `allocator_activated` field will be set to false and QUADS will function as usual.
* To let QUADS know about the presence of an external resource alloctor, set value of `allocator_activated` to true.

# Step 2: Set up and Initialize client library of HIL.

* Client library of HIL is a wrapper that abstracts away all the rest call related complexity of interacting with the HIL server. It pre-processes the input and manages communication (output and errors) on behalf of the client. 

* Copy the client library from [HIL client library code](https://github.com/CCI-MOC/hil/tree/master/hil/client) to the [QUADS library location](../lib/)

* The [initialization script](#initialize_hil.py) fetches HIL specific parameters from configuration file of QUADS and does the necessary setup that is required to communicate with the HIL server. 


