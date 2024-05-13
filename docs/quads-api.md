# QUADS API Documentation

We provide a RESTful API based on Flask endpoints with QUADS.

* [Using the QUADS REST API](#using-the-quads-rest-api)
    * [Authentication](#authentication)
    * [API GET Operations](#api-get-operations)
    * [API POST Operations](#api-post-operations)
    * [Working Examples](#working-examples)
    * [More Examples with API POST](#more-examples-with-api-post)

## Authentication
* The QUADS API uses a simple token-based authentication mechanism.
* You can generate a token doing a login with basic auth and then using the token for subsequent requests.
* All GET requests are open with no authentication required.
* All other requests require a valid token to be passed in the `Authorization` header.

### Example login request:

```bash
curl -X POST -u $USERNAME:$PASSWORD -H 'accept: application/json' 'http://localhost/api/v3/login/'
```

  - Response:
```json
{
    "auth_token":"7h1515@v3ryl0n6@ndcr1p71c70k3n",
    "message":"Successful login",
    "status":"success",
    "status_code":201
}
```

## Using the QUADS REST API
* All QUADS actions under the covers uses the REST API v3
* This is a local systemd service you can start and interact with and listens on localhost `TCP/8080`

```bash
systemctl enable quads-server.service
systemctl start quads-server.service
```

  - All the argparse and normal QUADS sub-commands are supported and will accept http `GET` and `POST` actions in a JSON response body.
    - Example: getting the equivalent of `quads --ls-hosts` via curl

```bash
curl http://localhost/api/v3/hosts
```

You'll then see a JSON response back.
```json
[{"broken":false,"build":false,"cloud":{"id":1,"last_redefined":"Tue, 30 Apr 2024 12:07:05 GMT","name":"cloud01"},"cloud_id":1,"created_at":"Tue, 30 Apr 2024 12:07:15 GMT","default_cl
oud":{"id":1,"last_redefined":"Tue, 30 Apr 2024 12:07:05 GMT","name":"cloud01"},"default_cloud_id":1,"host_type":"vendor","id":1,"last_build":null,"model":"5039MS","name":"example.com","retired":false,"switch_config_applied":false,"validated":false},...}]
```

You'll probably want to jsonify this to make it more readable:

```bash
curl http://localhost/api/v3/hosts | python -m json.tool
```

```json
[
    {
        "broken": false,
        "build": false,
        "cloud": {
            "id": 1,   
            "last_redefined": "Tue, 30 Apr 2024 12:07:05 GMT",
            "name": "cloud01"
        },
        "cloud_id": 1, 
        "created_at": "Tue, 30 Apr 2024 12:07:15 GMT",
        "default_cloud": {
            "id": 1,   
            "last_redefined": "Tue, 30 Apr 2024 12:07:05 GMT",
            "name": "cloud01"
        },
        "default_cloud_id": 1,
        "host_type": "vendor",
        "id": 1,
        "last_build": null,
        "model": "5039MS",
        "name": "example.com",
        "retired": false,
        "switch_config_applied": false,
        "validated": false
    },
    ...
]
```

### API GET Operations
* The following commands can be queried via curl or some other http mechanism to do basic metadata queries:
  * ```curl http://localhost/```
    - `/api/v3/version`             Obtain QUADS current version
    - `/api/v3/hosts`               Obtain a list of hosts managed by QUADS
    - `/api/v3/clouds`              Obtain list of cloud assignments
    - `/api/v3/schedules`           Retrieve a list of all schedules
    - `/api/v3/available`           List available hosts, usually used with `--schedule-start YYYY-MM-DD HH` and `--schedule-end YYYY-MM-DD HH`
    - `/api/v3/interfaces`          List interfaces of QUADS host(s)
    - `/api/v3/clouds/summary`      Obtain a full summary of clouds, tickets, descriptions
    - `/api/v3/moves`               Obtain a list of hosts with their current and future clouds

### API POST Operations
* The following construct can be used via http ```POST``` to receive more detailed data by providing granular criteria to return JSON body data:
  * You can combine one of many POST query types with multiple POST metadata objects.
  * There is limited support for data modification via POST as well documented below.
  * Valid POST URI queries
    - ```/api/v3/hosts```        Same as `quads-cli --define-host`, used for defining a new host.
    - ```/api/v3/clouds```       Same as `quads-cli --define-cloud` for creating/updating a cloud environment.
    - ```/api/v3/schedules```    AKA _add host schedule_ used for adding a new host schedule.
    - ```/api/v3/interfaces```   Add an interface to a QUADS-managed host

## Working Examples:
### Query hosts on a specific cloud
```bash
curl http://localhost/api/v3/hosts?cloud=cloud04 | python3 -m json.tool
```

```json
[
    {
        "broken": false,
        "build": false,
        "cloud": {
            "id": 1,   
            "last_redefined": "Tue, 30 Apr 2024 12:07:05 GMT",
            "name": "cloud04"
        },
        "cloud_id": 1, 
        "created_at": "Tue, 30 Apr 2024 12:07:15 GMT",
        "default_cloud": {
            "id": 1,   
            "last_redefined": "Tue, 30 Apr 2024 12:07:05 GMT",
            "name": "cloud01"
        },
        "default_cloud_id": 1,
        "host_type": "vendor",
        "id": 1,
        "last_build": null,
        "model": "5039MS",
        "name": "example.com",
        "retired": false,
        "switch_config_applied": false,
        "validated": false
    },
    ...
]
```

### Query a host schedule

```bash
curl http://localhost/api/v3/schedules?host=host01.example.com | python3 -m json.tool
```
  - We can see there is no schedule for this host:
```json
[]
```

  - Before we create a schedule we must have an active assignment
```bash
curl -X 'POST' \
  'http://localhost/api/v3/assignments/' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer $TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
      "active": true,
      "ccuser": [
        "edroste",
        "kgodel"
      ],
      "cloud": "cloud04",
      "description": "Short description here",
      "owner": "jsbach",
      "provisioned": true,
      "qinq": 1,
      "ticket": "3464",
      "validated": true,
      "wipe": true
    }'
```
  - Response:
```json
{
  "active": true,
  "ccuser": [],
  "cloud": {
    "id": 6,
    "last_redefined": "Mon, 13 May 2024 08:53:31 GMT",
    "name": "cloud04"
  },
  "cloud_id": 6,
  "created_at": "Mon, 13 May 2024 09:06:00 GMT",
  "description": "Short description here",
  "id": 4,
  "notification": {
    "assignment_id": 4,
    "fail": false,
    "five_days": false,
    "id": 4,
    "initial": false,
    "one_day": false,
    "pre": false,
    "pre_initial": false,
    "seven_days": false,
    "success": false,
    "three_days": false
  },
  "owner": "jsbach",
  "provisioned": false,
  "qinq": 1,
  "ticket": "3464",
  "validated": false,
  "vlan_id": null,
  "wipe": true
}
```

  - Once we have an active assignment we can add a new schedule and then query
```bash
curl -X 'POST' \
  'http://localhost/api/v3/schedules/' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer $TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "assignment_id": 4,
  "start": "2024-06-02 22:00",
  "end": "2024-07-02 22:00",
  "hostname": "host01.example.com",
  "cloud": "cloud04"
}'
```

  - Response:
```json
{
  "assignment": {
    "active": true,
    "ccuser": [],
    "cloud": {
      "id": 6,
      "last_redefined": "Mon, 13 May 2024 08:53:31 GMT",
      "name": "cloud04"
    },
    "cloud_id": 6,
    "created_at": "Mon, 13 May 2024 09:06:00 GMT",
    "description": "Short description here",
    "id": 4,
    "notification": {
      "assignment_id": 4,
      "fail": false,
      "five_days": false,
      "id": 4,
      "initial": false,
      "one_day": false,
      "pre": false,
      "pre_initial": false,
      "seven_days": false,
      "success": false,
      "three_days": false
    },
    "owner": "jsbach",
    "provisioned": false,
    "qinq": 1,
    "ticket": "3464",
    "validated": false,
    "vlan_id": null,
    "wipe": true
  },
  "assignment_id": 4,
  "build_end": null,
  "build_start": null,
  "created_at": "Mon, 13 May 2024 09:12:42 GMT",
  "end": "Tue, 02 Jul 2024 22:00:00 GMT",
  "host": {
    "broken": false,
    "build": false,
    "cloud": {
      "id": 1,
      "last_redefined": "Tue, 30 Apr 2024 12:07:05 GMT",
      "name": "cloud01"
    },
    "cloud_id": 1,
    "created_at": "Tue, 30 Apr 2024 12:07:28 GMT",
    "default_cloud": {
      "id": 1,
      "last_redefined": "Tue, 30 Apr 2024 12:07:05 GMT",
      "name": "cloud01"
    },
    "default_cloud_id": 1,
    "disks": [
      {
        "count": 1,
        "disk_type": "sata",
        "host_id": 15,
        "id": 8,
        "size_gb": 480
      }
    ],
    "host_type": "vendor",
    "id": 15,
    "interfaces": [
      {
        "bios_id": null,
        "host_id": 15,
        "id": 25,
        "mac_address": "0c:c4:7a:ea:8e:2c",
        "maintenance": false,
        "name": "em1",
        "pxe_boot": false,
        "speed": 10,
        "switch_ip": "10.1.34.235",
        "switch_port": "xe-0/0/8:0",
        "vendor": "Intel Corporation"
      },
      {
        "bios_id": null,
        "host_id": 15,
        "id": 26,
        "mac_address": "0c:c4:7a:ea:8e:2d",
        "maintenance": false,
        "name": "em2",
        "pxe_boot": true,
        "speed": 10,
        "switch_ip": "10.1.34.235",
        "switch_port": "xe-0/0/8:1",
        "vendor": "Intel Corporation"
      },
      {
        "bios_id": null,
        "host_id": 15,
        "id": 27,
        "mac_address": "0c:c4:7a:ea:8e:2e",
        "maintenance": false,
        "name": "em3",
        "pxe_boot": false,
        "speed": 10,
        "switch_ip": "10.1.34.235",
        "switch_port": "xe-0/0/8:2",
        "vendor": "Intel Corporation"
      },
      {
        "bios_id": null,
        "host_id": 15,
        "id": 28,
        "mac_address": "0c:c4:7a:ea:8e:2f",
        "maintenance": false,
        "name": "em4",
        "pxe_boot": false,
        "speed": 10,
        "switch_ip": "10.1.34.235",
        "switch_port": "xe-0/0/8:3",
        "vendor": "Intel Corporation"
      }
    ],
    "last_build": null,
    "model": "1029P",
    "name": "host01.example.com",
    "retired": false,
    "switch_config_applied": false,
    "validated": false
  },
  "host_id": 15,
  "id": 16,
  "start": "Sun, 02 Jun 2024 22:00:00 GMT"
}
```

  - Now query again:

```bash
curl http://localhost/api/v3/schedules?host=host01.example.com | python3 -m json.tool
```
```json
[
    {
      "assignment": {
        "active": true,
        "ccuser": [],
        "cloud": {
          "id": 6,
          "last_redefined": "Mon, 13 May 2024 08:53:31 GMT",
          "name": "cloud04"
        },
        "cloud_id": 6,
        "created_at": "Mon, 13 May 2024 09:06:00 GMT",
        "description": "Short description here",
        "id": 4,
        "notification": {
          "assignment_id": 4,
          "fail": false,
          "five_days": false,
          "id": 4,
          "initial": false,
          "one_day": false,
          "pre": false,
          "pre_initial": false,
          "seven_days": false,
          "success": false,
          "three_days": false
        },
        "owner": "jsbach",
        "provisioned": false,
        "qinq": 1,
        "ticket": "3464",
        "validated": false,
        "vlan_id": null,
        "wipe": true
      },
      "assignment_id": 4,
      "build_end": null,
      "build_start": null,
      "created_at": "Mon, 13 May 2024 09:12:42 GMT",
      "end": "Tue, 02 Jul 2024 22:00:00 GMT",
      "host": {
        "broken": false,
        "build": false,
        "cloud": {
          "id": 1,
          "last_redefined": "Tue, 30 Apr 2024 12:07:05 GMT",
          "name": "cloud01"
        },
        "cloud_id": 1,
        "created_at": "Tue, 30 Apr 2024 12:07:28 GMT",
        "default_cloud": {
          "id": 1,
          "last_redefined": "Tue, 30 Apr 2024 12:07:05 GMT",
          "name": "cloud01"
        },
        "default_cloud_id": 1,
        "disks": [
          {
            "count": 1,
            "disk_type": "sata",
            "host_id": 15,
            "id": 8,
            "size_gb": 480
          }
        ],
        "host_type": "vendor",
        "id": 15,
        "interfaces": [
          {
            "bios_id": null,
            "host_id": 15,
            "id": 25,
            "mac_address": "0c:c4:7a:ea:8e:2c",
            "maintenance": false,
            "name": "em1",
            "pxe_boot": false,
            "speed": 10,
            "switch_ip": "10.1.34.235",
            "switch_port": "xe-0/0/8:0",
            "vendor": "Intel Corporation"
          },
          {
            "bios_id": null,
            "host_id": 15,
            "id": 26,
            "mac_address": "0c:c4:7a:ea:8e:2d",
            "maintenance": false,
            "name": "em2",
            "pxe_boot": true,
            "speed": 10,
            "switch_ip": "10.1.34.235",
            "switch_port": "xe-0/0/8:1",
            "vendor": "Intel Corporation"
          },
          {
            "bios_id": null,
            "host_id": 15,
            "id": 27,
            "mac_address": "0c:c4:7a:ea:8e:2e",
            "maintenance": false,
            "name": "em3",
            "pxe_boot": false,
            "speed": 10,
            "switch_ip": "10.1.34.235",
            "switch_port": "xe-0/0/8:2",
            "vendor": "Intel Corporation"
          },
          {
            "bios_id": null,
            "host_id": 15,
            "id": 28,
            "mac_address": "0c:c4:7a:ea:8e:2f",
            "maintenance": false,
            "name": "em4",
            "pxe_boot": false,
            "speed": 10,
            "switch_ip": "10.1.34.235",
            "switch_port": "xe-0/0/8:3",
            "vendor": "Intel Corporation"
          }
        ],
        "last_build": null,
        "model": "1029P",
        "name": "host01.example.com",
        "retired": false,
        "switch_config_applied": false,
        "validated": false
      },
      "host_id": 15,
      "id": 16,
      "start": "Sun, 02 Jun 2024 22:00:00 GMT"
    }
]
```

## More Examples with API POST

### Define a Host via API POST
```bash
curl -X 'POST' \
  'http://localhost/api/v3/hosts/' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer $TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "default_cloud": "cloud01",
  "host_type": "vendor",
  "model": "r640",
  "name": "host.example.com"
}'
```

  - Response:
```json
{
  "broken": false,
  "build": false,
  "cloud": {
    "id": 1,
    "last_redefined": "Tue, 30 Apr 2024 12:07:05 GMT",
    "name": "cloud01"
  },
  "cloud_id": 1,
  "created_at": "Mon, 13 May 2024 09:19:00 GMT",
  "default_cloud": {
    "id": 1,
    "last_redefined": "Tue, 30 Apr 2024 12:07:05 GMT",
    "name": "cloud01"
  },
  "default_cloud_id": 1,
  "host_type": "vendor",
  "id": 18,
  "last_build": null,
  "model": "R640",
  "name": "host.example.com",
  "retired": false,
  "switch_config_applied": false,
  "validated": false
}
```
