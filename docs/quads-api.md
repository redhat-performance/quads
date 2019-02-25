# QUADS API Documentation

We provide a RESTful API based on CherryPy endpoints with QUADS.

* [Using the QUADS JSON API](#quads-api-documentation)
    * [API GET Operations](#api-get-operations)
    * [API POST Operations](#api-post-operations)
    * [Working Examples](#working-examples)
    * [More Examples with API POST](#more-examples-with-api-post)

## Using the QUADS JSON API
* All QUADS actions under the covers uses the JSON API v2
* This is an optional local systemd service you can start and interact with and listens on localhost ```TCP/8080```

```
cp systemd/quads-server.service /etc/systemd/system/quads-server.service
systemctl enable quads-server.service
systemctl start quads-server.service
```

  - All of the argparse and normal QUADS sub-commands are supported and will accept http ```GET``` and ```POST``` actions in a JSON response body.
    - Example: getting the equivalent of ```quads --ls-hosts``` via curl

```
curl -X GET -H 'Content-Type: application/json' http://127.0.0.1:8080/api/v1/lshosts
```

You'll then see a JSON response back.
```
{"hosts": ["b08-h13-r620.rdu.openstack.engineering.example.com", "b08-h14-r620.rdu.openstack.engineering.example.com", "b08-h15-r620.rdu.openstack.engineering.example.com", "b08-h17-r620.rdu.openstack.engineering.example.com", "b08-h18-r620.rdu.openstack.engineering.example.com", "b08-h19-r620.rdu.openstack.engineering.example.com", "b08-h21-r620.rdu.openstack.engineering.example.com"]}
```

### API GET Operations
* The following commands can be queried via curl or some other http mechanism to do basic metadata queries:
  * ```curl -X GET -H 'Content-Type: application/json' http://127.0.0.1:8080```
    - ```/api/v1/lshosts```    Obtain a list of hosts managed by QUADS
    - ```/api/v1/lsclouds```   Obtain list of cloud assignments
    - ```/api/v1/lsowner```    Retrieve a list of current system assignment owners
    - ```/api/v1/lsccusers```  List the cc-users associated for assignments
    - ```/api/v1/lstickets```  Obtain the ticket numbers to assignment mappings
    - ```/api/v1/lsqinq```     List the qinq VLAN mode (0|1) per cloud assignment

### API POST Operations
* The following construct can be used via http ```POST``` to receive more detailed data by providing granular criteria to return JSON body data:
  * You can combine one of many POST query types with multiple POST metadata objects.
  * There is limited support for data modification via POST as well documented below.
  * Valid POST URI queries
    - ```/api/v1/lsowner```
    - ```/api/v1/lsccusers```
    - ```/api/v1/lstickets```
    - ```/api/v1/lsqinq```
    - ```/api/v1/host```      Can also be used for defining/updating a host.
    - ```/api/v1/cloud```     Can also be used for defining/updating a cloud assignment.
    - ```/api/v1/ahs```       AKA _add host schedule_ used for adding a new host schedule.
    - ```/api/v1/rhs```       AKA _remove host schedule_ used for removing a host schedule.
    - ```/api/v1/mhs```       AKA _modify host schedule_ used for modifying a host schedule.
    - ```/api/v1/moves```     Reports what would be moved on a given date.

  * Valid POST object filters:
    - ```-d cloud=cloud0X```
    - ```-d cloudonly=cloud0X```
    - ```-d 'date=2018-08-08 22:00'```
    - ```-d statedir=/path/to/quads/datadir```
    - ```-d fullsummary=True/False```
    - ```-d host=c10-h33-r630.rdu.openstack.engineering.example.com```

* Constructing an http POST example with multiple metadata objects:

```curl -X POST -H 'Content-Type: application/json'``` ```-d``` ```quadsvariable=value``` ```-d``` ```quadsvariable=value``` ```http://127.0.0.1:8080/api/v1/object```

### Working Examples:
  - Query the owners of cloud02 only
```
curl -X POST -H 'Content-Type: application/json' -d cloudonly=cloud02  http://127.0.0.1:8080/api/v1/lsowners ; echo
```

```
{"owner": ["epresley"]}
```
  - Use the Query Object to Obtain Details
```
curl -X POST http://localhost:8080/api/v1/query -d host=c01-h01-r620.rdu.openstack.engineering.example.com -d lsschedule=True -H 'Content-Type: application/json'
```

```
{"result": ["Default cloud: cloud01", "Current cloud: cloud01", "Defined schedules:", "  0| start=2016-10-17 00:00,end=2016-12-21 17:00,cloud=cloud04", "  1| start=2016-12-21 17:00,end=2017-0
08", "  2| start=2017-02-09 05:00,end=2017-03-06 05:00,cloud=cloud02", "  3| start=2017-03-20 05:00,end=2017-04-03 05:00,cloud=cloud03", "  4| start=2017-02-03 19:00,end=2017-02-09 05:00,clou
t=2017-03-06 05:00,end=2017-03-20 05:00,cloud=cloud16", "  6| start=2017-04-03 05:00,end=2017-05-01 05:00,cloud=cloud02", "  7| start=2017-06-18 22:00,end=2017-07-02 22:00,cloud=cloud05", "
:00,end=2017-05-28 22:00,cloud=cloud07"]}
```

  - Query all of the future move actions on the day and time ```2018-01-01 22:00```
```
curl -X POST -H 'Content-Type: application/json' -d 'date=2018-01-01 22:00' -d statedir=/opt/quads/data http://127.0.0.1:8080/api/v1/moves ; echo
```

```
{"result": [{"current": "cloud14", "new": "cloud01", "host": "b08-h13-r620.rdu.openstack.example.com"}, {"current": "cloud14", "new": "cloud01"}]}
```

### More Examples with API POST

  - Define a Host via API POST
```
curl -X POST http://localhost:8080/api/v1/host -d host=c10-h33-r630.rdu.openstack.example.com -d cloud=cloud01 -d force=False -H 'Content-Type: application/json'
```

  - Add a new Cloud Assignment via API POST
```
curl -X POST http://localhost:8080/api/v1/cloud -d cloud=cloud03 -d description='Some project' -H 'Content-Type: application/json'
```

  - Modify a Cloud Assignment via API POST
```
curl -X POST http://localhost:8080/api/v1/cloud -d cloud=cloud03 -d description='New Updated Description' -d force=True -H 'Content-Type: application/json'
```

  - Add a new Host Schedule via API POST
```
curl -X POST http://localhost:8080/api/v1/ahs -d host=c01-h01-r620.rdu.openstack.example.com -d 'start=2017-09-01 22:00' -d 'end=2017-09-30 22:00' -d 'cloud=cloud04' -H 'Content-Type: application/json'
```

  - Modify a Host Schedule via API POST
    - At least one of ```start=``` ```end=``` or ```cloud=``` are required with modifications.
```
curl -X POST http://localhost:8080/api/v1/mhs -d host=c01-h01-r620.rdu.openstack.example.com -d 'start=2017-09-01 22:00' -d 'end=2017-09-30 22:00' -d 'cloud=cloud04' -H 'Content-  Type: application/json'
```

  - Remove a Host Schedule via API POST
    - ```schedule=``` is the numeric value of the target schedule, you can use the ```query``` object to determine this (or ```--ls-schedule``` via cli or ```/opt/quads/bin/quads-cli```
```
curl -X POST http://localhost:8080/api/v1/rhs -d host=c01-h01-r620.rdu.openstack.example.com -d schedule=1
```

* Using quads-cli
  - ```/opt/quads/bin/quads-cli``` is a front-end to the ```bin/quads-server``` JSON API.
  - ```/opt/quads/bin/quads-cli``` interacts with ```/opt/quads/bin/quads-server``` exactly like the normal ```/opt/quads/bin/quads-cli`` so you can utilize the same documentation above.
