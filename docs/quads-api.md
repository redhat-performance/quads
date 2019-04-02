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
[{"_id": {"$oid": "5ca3750283a3de000744b491"}, "name": "host01.example.com", "cloud": {"$oid": "5ca374f683a3de000744b48f"}, "host_type": "util", "interfaces": [], "nullos": true, "build": false}, {"_id": {"$oid": "5ca3781e83a3de000744b492"}, "name": "host02.example.com", "cloud": {"$oid": "5ca374f683a3de000744b48f"}, "host_type": "util", "interfaces": [], "nullos": true, "build": false}
```

You'll probably want to jsonify this to make it more readable:

```
curl -qs -X GET -H 'Content-Type: application/json' http://127.0.0.1:8080/api/v2/host | python3 -m json.tool
```

```
[
    {
        "_id": {
            "$oid": "5ca3750283a3de000744b491"
        },
        "name": "host01.example.com",
        "cloud": {
            "$oid": "5ca374f683a3de000744b48f"
        },
        "host_type": "util",
        "interfaces": [],
        "nullos": true,
        "build": false
    },
    {
        "_id": {
            "$oid": "5ca3781e83a3de000744b492"
        },
        "name": "host02.example.com",
        "cloud": {
            "$oid": "5ca374f683a3de000744b48f"
        },
        "host_type": "util",
        "interfaces": [],
        "nullos": true,
        "build": false
    }
]
```

### API GET Operations
* The following commands can be queried via curl or some other http mechanism to do basic metadata queries:
  * ```curl -X GET -H 'Content-Type: application/json' http://127.0.0.1:8080```
    - `/api/v2/host`        Obtain a list of hosts managed by QUADS
    - `/api/v2/cloud`       Obtain list of cloud assignments
    - `/api/v2/owner`       Retrieve a list of current system assignment owners
    - `/api/v2/cloudowner`  Retrieve a list of current cloud environment owners
    - `/api/v2/ccuser`      List the cc-users associated for assignments
    - `/api/v2/ticket`      Obtain the ticket numbers to assignment mappings
    - `/api/v2/qinq`        List the qinq VLAN mode (0|1) per cloud assignment
    - `/api/v2/wipe`        List what cloud environments are set to wipe systems or not on new assignment.
    - `/api/v2/available`   List available hosts, usually used with `--schedule-start YYYY-MM-DD HH` and `--schedule-end YYYY-MM-DD HH`
    - `/api/v2/interface`   List interfaces of QUADS host(s)
    - `/api/v2/fullsummary` Obtain a full summary of clouds, tickets, descriptions

### API POST Operations
* The following construct can be used via http ```POST``` to receive more detailed data by providing granular criteria to return JSON body data:
  * You can combine one of many POST query types with multiple POST metadata objects.
  * There is limited support for data modification via POST as well documented below.
  * Valid POST URI queries
    - ```/api/v2/hostresource``` Same as `quads-cli --define-host`, used for defining a new host.
    - ```/api/v2/cloudresource``` Same as `quads-cli --define-cloud` for creating/updating a cloud environment.
    - ```/api/v2/addschedule``    AKA _add host schedule_ used for adding a new host schedule.
    - ```/api/v2/rmschedule```    AKA _remove host schedule_ used for removing a host schedule.
    - ```/api/v2/modschedule```   AKA _modify host schedule_ used for modifying a host schedule.
    - ```/api/v2/rmhost```       Removes a QUADS-managed host from QUADS
    - ```/api/v2/addinterface``` Add an interface to a QUADS-managed host
    - ```/api/v2/rminterface```  Remove an interface from a QUADS-managed host
    - ```/api/v2/rmcloud```      Remove a defined cloud environment
    - ```/api/v2/movehosts```    Initiate move of hosts if they are due, used with `--dry-run` to show what would happen.

  * Valid POST object filters:
    - ```-d cloud=cloud0X```
    - ```-d cloudonly=cloud0X```
    - ```-d 'date=2018-08-08 22:00'```
    - ```-d fullsummary=True/False```
    - ```-d host=c10-h33-r630.example.com```
    - ```-d 'start=2019-04-02 22:00'```
    - ```-d 'end=2019-04-03 22:00'```
    - ```-d 'ifmac=fe:54:00:a4:e9:8d'```
    - ```-d 'ifip=10.1.20.20'```
    - ```-d 'ifport=xe-0/0/3:0'```
    - ```-d dryrun=True/False```
    - ```-d vlan=integer```

* Constructing an http POST example with multiple metadata objects:

```curl -X POST -H 'Content-Type: application/json'``` ```-d``` ```quadsvariable=value``` ```-d``` ```quadsvariable=value``` ```http://127.0.0.1:8080/api/v2/object```

### Working Examples:
  - Query the hosts belonging to cloud01 only
```
curl -qs -X GET -H 'Content-Type: application/json' -d cloudonly=cloud01 http://127.0.0.1:8080/api/v2/host | python3 -m json.tool
```

```
[
    {
        "_id": {
            "$oid": "5ca3750283a3de000744b491"
        },
        "name": "host01.example.com",
        "cloud": {
            "$oid": "5ca374f683a3de000744b48f"
        },
        "host_type": "util",
        "interfaces": [],
        "nullos": true,
        "build": false
    },
    {
        "_id": {
            "$oid": "5ca3781e83a3de000744b492"
        },
        "name": "host02.example.com",
        "cloud": {
            "$oid": "5ca374f683a3de000744b48f"
        },
        "host_type": "util",
        "interfaces": [],
        "nullos": true,
        "build": false
    }
]

```

  - Query a host schedule

```
/opt/quads# curl -qs -X GET -H 'Content-Type: application/json' http://127.0.0.1:8080/api/v2/schedule?host=host01.example.com | python3 -m json.tool
```
  - We can see there is no schedule for this host:
```
[]
```
  - Let's add one and then query
```
quads-cli --add-schedule --host host01.example.com --schedule-start "2019-06-01 22:00" --schedule-end "2019-06-02 22:00" --schedule-cloud cloud02
['Added schedule for host01.example.com on cloud02']
```
  - Now query again:

```
curl -qs -X GET -H 'Content-Type: application/json' http://127.0.0.1:8080/api/v2/schedule?host=host01.example.com | python3 -m json.tool
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
curl -X POST -H 'Content-Type: application/json' -d 'Content-Length: 0' 'http://127.0.0.1:8080/api/v2/cloud?name=cloud09&description=some+other+cloud&owner=someone&ticket=000000&force=True'
```

  - Define a new cloud environment via API POST
```
curl -X POST -H 'Content-Type: application/json' -d 'Content-Length: 0' 'http://127.0.0.1:8080/api/v2/cloud?name=cloud09&description=some+other+cloud&owner=someone&ticket=000000'
```

  - Add a new Host Schedule via API POST
```
curl -X POST 'http://localhost:8080/api/v2/schedule?host=host01.example.com&start=2019-09-01+22:00&end=2019-09-30+22:00&cloud=cloud02' -H 'Content-Type: application/json' -d 'Content-Length: 0'
```
