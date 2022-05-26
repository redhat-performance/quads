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
curl -X GET -H 'Content-Type: application/json' http://127.0.0.1:8080/api/v2/host
```

You'll then see a JSON response back.
```
[{"_id":{"$oid":"5c82b3a90f767d000692ad48"},"name":"host01.example.com","cloud":{"$oid":"5c82b3660f767d000692acf7"},"host_type":"vendor","interfaces":[{"name":"em1","mac_address":"00:00:00:5e:84:90","switch_ip":"10.1.34.248","switch_port":"et-0/0/2:0"},{"name":"em2","mac_address":"00:00:00:5e:84:91","switch_ip":"10.1.34.248","switch_port":"et-0/0/2:1"}],"nullos":true,"build":false,"last_build":{"$date":1552923007391}},{"_id":{"$oid":"5c82b3a90f767d000692ad49"},"name":"host02.example.com","cloud":{"$oid":"5c82b3660f767d000692acf7"},"host_type":"vendor","interfaces":[{"name":"em1","mac_address":"00:00:00:5e:84:92","switch_ip":"10.1.34.248","switch_port":"et-0/0/2:0"},{"name":"em2","mac_address":"00:00:00:5e:84:93","switch_ip":"10.1.34.248","switch_port":"et-0/0/2:1"}],"nullos":true,"build":false,"last_build":{"$date":1552923007391}}]
```

You'll probably want to jsonify this to make it more readable:

```
curl -qs -X GET -H 'Content-Type: application/json' http://127.0.0.1:8080/api/v2/host | python3 -m json.tool
```

```
[[
    {
        "_id": {
            "$oid": "5c82b3a90f767d000692ad48"
        },
        "name": "host01.example.com",
        "cloud": {
            "$oid": "5c82b3660f767d000692acf7"
        },
        "host_type": "vendor",
        "interfaces": [
            {
                "name": "em1",
                "mac_address": "00:00:00:5e:84:90",
                "switch_ip": "10.1.34.248",
                "switch_port": "et-0/0/2:0"
            },
            {
                "name": "em2",
                "mac_address": "00:00:00:5e:84:91",
                "switch_ip": "10.1.34.248",
                "switch_port": "et-0/0/2:1"
            }
        ],
        "nullos": true,
        "build": false,
        "last_build": {
            "$date": 1552923007391
        }
    },    {
        "_id": {
            "$oid": "5c82b3a90f767d000692ad49"
        },
        "name": "host02.example.com",
        "cloud": {
            "$oid": "5c82b3660f767d000692acf7"
        },
        "host_type": "vendor",
        "interfaces": [
            {
                "name": "em1",
                "mac_address": "00:00:00:5e:84:92",
                "switch_ip": "10.1.34.248",
                "switch_port": "et-0/0/2:0"
            },
            {
                "name": "em2",
                "mac_address": "00:00:00:5e:84:93",
                "switch_ip": "10.1.34.248",
                "switch_port": "et-0/0/2:1"
            }
        ],
        "nullos": true,
        "build": false,
        "last_build": {
            "$date": 1552923007391
        }
    }
]
```

### API GET Operations
* The following commands can be queried via curl or some other http mechanism to do basic metadata queries:
  * ```curl http://127.0.0.1:8080```
    - `/api/v2/version`             Obtain QUADS current version
    - `/api/v2/host`                Obtain a list of hosts managed by QUADS
    - `/api/v2/cloud`               Obtain list of cloud assignments
    - `/api/v2/owner`               Retrieve a list of current system assignment owners
    - `/api/v2/ccuser`              List the cc-users associated for assignments
    - `/api/v2/ticket`              Obtain the ticket numbers to assignment mappings
    - `/api/v2/qinq`                List the qinq VLAN mode (0|1) per cloud assignment
    - `/api/v2/wipe`                List what cloud environments are set to wipe systems or not on new assignment.
    - `/api/v2/schedule`            Retrieve a list of all schedules
    - `/api/v2/current_schedule`    Retrieve a list of all are currently scheduled
    - `/api/v2/available`           List available hosts, usually used with `--schedule-start YYYY-MM-DD HH` and `--schedule-end YYYY-MM-DD HH`
    - `/api/v2/interfaces`          List interfaces of QUADS host(s)
    - `/api/v2/summary`             Obtain a full summary of clouds, tickets, descriptions
    - `/api/v2/moves`               Obtain a list of hosts with their current and future clouds

### API POST Operations
* The following construct can be used via http ```POST``` to receive more detailed data by providing granular criteria to return JSON body data:
  * You can combine one of many POST query types with multiple POST metadata objects.
  * There is limited support for data modification via POST as well documented below.
  * Valid POST URI queries
    - ```/api/v2/host```        Same as `quads-cli --define-host`, used for defining a new host.
    - ```/api/v2/cloud```       Same as `quads-cli --define-cloud` for creating/updating a cloud environment.
    - ```/api/v2/schedule```    AKA _add host schedule_ used for adding a new host schedule.
    - ```/api/v2/interfaces```  Add an interface to a QUADS-managed host

  * Valid POST object filters:
    - ```-d 'cloud=cloud0X'```
    - ```-d 'date=2018-08-08 22:00'```
    - ```-d 'host=c10-h33-r630.example.com'```
    - ```-d 'host_type=vendor'```
    - ```-d 'start=2019-04-02 22:00'```
    - ```-d 'end=2019-04-03 22:00'```
    - ```-d 'vlan=601'```
    - ```-d 'index=1'```
    - ```-d 'force=true'```
    - ```-d 'name=em1'```
    - ```-d 'mac_address=00:00:00:00:00:00'```
    - ```-d 'switch_ip=192.168.35.35'```
    - ```-d 'switch_port=et-0/0/2:1'```
    - ```-d 'description=some other cloud'```
    - ```-d 'owner=nobody'```
    - ```-d 'cc_user=this that'```
    - ```-d 'qinq=1'```
    - ```-d 'wipe=true'```
    - ```-d 'ticket=000000'```


* Constructing an http POST example with multiple metadata objects:

```
curl -X POST -H 'Content-Type: application/json' \
-d quadsvariable=value \
-d quadsvariable=value \
http://127.0.0.1:8080/api/v2/object
```

### Working Examples:
  - Query the hosts belonging to cloud09 only
```
curl http://127.0.0.1:8080/api/v2/host?cloud=cloud09 | python3 -m json.tool
```

```
[
    {
        "_id": {
            "$oid": "5c82b3a90f767d000692ad48"
        },
        "name": "host01.example.com",
        "cloud": {
            "$oid": "5c82b3660f767d000692acf7"
        },
        "host_type": "vendor",
        "interfaces": [
            {
                "name": "em1",
                "mac_address": "00:00:00:5e:84:90",
                "switch_ip": "10.1.34.248",
                "switch_port": "et-0/0/2:0"
            },
            {
                "name": "em2",
                "mac_address": "00:00:00:5e:84:91",
                "switch_ip": "10.1.34.248",
                "switch_port": "et-0/0/2:1"
            }
        ],
        "nullos": true,
        "build": false,
        "last_build": {
            "$date": 1552923007391
        }
    },    {
        "_id": {
            "$oid": "5c82b3a90f767d000692ad49"
        },
        "name": "host02.example.com",
        "cloud": {
            "$oid": "5c82b3660f767d000692acf7"
        },
        "host_type": "vendor",
        "interfaces": [
            {
                "name": "em1",
                "mac_address": "00:00:00:5e:84:92",
                "switch_ip": "10.1.34.248",
                "switch_port": "et-0/0/2:0"
            },
            {
                "name": "em2",
                "mac_address": "00:00:00:5e:84:93",
                "switch_ip": "10.1.34.248",
                "switch_port": "et-0/0/2:1"
            }
        ],
        "nullos": true,
        "build": false,
        "last_build": {
            "$date": 1552923007391
        }
    }
]
```

  - Query a host schedule

```
/opt/quads# curl http://127.0.0.1:8080/api/v2/schedule?host=host01.example.com | python3 -m json.tool
```
  - We can see there is no schedule for this host:
```
[]
```

  - Let's add one and then query
```
curl -X POST 'http://localhost:8080/api/v2/schedule?host=host01.example.com&start=2019-09-01+22:00&end=2019-09-30+22:00&cloud=cloud02' -H 'Content-Type: application/json' -d 'Content-Length: 0'
{"result": ['Added schedule for host01.example.com on cloud02']}
```

  - Now query again:

```
curl http://127.0.0.1:8080/api/v2/schedule?host=host01.example.com | python3 -m json.tool
```
```
[
    {
        "_id": {
            "$oid": "5caba4766eed620006bb6735"
        },
        "cloud": {
            "$oid": "5ca3843083a3de00069d1461"
        },
        "host": {
            "$oid": "5ca3750283a3de000744b491"
        },
        "start": {
            "$date": 1559426400000
        },
        "end": {
            "$date": 1559512800000
        },
        "index": 1
    }
]
```

### More Examples with API POST

  - Define a Host via API POST
```
curl -X POST -H 'Content-Type: application/json' -d 'Content-Length: 0' 'http://127.0.0.1:8080/api/v2/host?name=host02.example.com&cloud=cloud01&host_type=vendor&force=True'
{"result": ["Created host host02.example.com"]}
```

  - Define a new cloud environment via API POST
```
curl -X POST -H 'Content-Type: application/json' -d 'Content-Length: 0' 'http://127.0.0.1:8080/api/v2/cloud?name=cloud09&description=some+other+cloud&owner=someone&ticket=000000'
{"result": ["Created cloud cloud09"]}(
```
