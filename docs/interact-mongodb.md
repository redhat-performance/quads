## Interacting with MongoDB

   * [Interacting with MongoDB](#interacting-with-mongodb)
     * [Getting Started](#getting-started)
     * [Example: Get hosts by switch port and switch ip](#example-get-hosts-by-switch-port-and-switch-ip)
     * [Example: Change the wipe value in MongoDB](#example-change-the-wipe-value-in-mongodb)
     * [Example: Querying Notification Values in MongoDB](#example-querying-notification-values-in-mongodb)
     * [Example: Query Multiple Values in MongoDB inside Collections](#example-query-multiple-values-in-mongodb-inside-collections)
     * [Example: Manually Validate Hosts](#example-manually-validate-hosts)
     * [Example: Manually moving a Host Cloud in MongoDB](#example-manually-moving-a-host-cloud-in-mongodb)
     * [Example: Toggling Individual Cloud Metadata Settings](#example-toggling-individual-cloud-metadata-settings)
     * [Example: Modifying cc-users](#example-modifying-cc-users)


* **NOTE**: For most of the below examples usage of `quads-cli --mod-cloud` supplants the need for making any changes in MongoDB post QUADS version `1.1.4`.  We'll leave these examples below for posterity or in the case they can be modeled to do something else useful otherwise.

### Getting Started

* Example:  Toggling the `wipe:` cloud value that determines whether new systems entering an environment should be reprovisioned or not.  In this example `cloud02` has the value of `wipe: 0` and we want to change this within Mongodb.

   - First run `mongo` to enter cli mode

```
# mongo
MongoDB shell version v4.0.3
connecting to: mongodb://127.0.0.1:27017
Implicit session: session { "id" : UUID("21a4cd3c-e191-4f03-b18c-dccdb55826b3") }
MongoDB server version: 4.0.3
```

   - Next, enter the database

```
> use quads
switched to db quads
```

### Example: Get hosts by switch port and switch ip

   - Query for all hosts which have interfaces to a specific switch port and switch ip

```
> db.host.find({"interfaces":{$elemMatch:{"switch_port":"xe-0/0/10:2", "ip_address":"10.1.1.10"}}})
{ "_id" : ObjectId("5c82b3660f767d000692acf7"), "name" : "host01.example.com", "cloud" : ObjectId("...
```

### Example: Change the wipe value in MongoDB

   - Query the cloud metadata for `cloud02`

```
> db.cloud.find({name: "cloud02"})
{ "_id" : ObjectId("5c82b3660f767d000692acf7"), "notified" : true, "validated" : true, "released" : true, "name" : "cloud02", "description" : "EL7 to EL8 Satellite Upgrade", "owner" : "ikaur", "ticket" : "490957", "qinq" : 0, "wipe" : false, "ccuser" : [ "psuriset" ], "provisioned" : true }
```

   - We want to change `wipe: false` to `wipe: true`

```
> db.cloud.update({name:"cloud02"}, {$set:{wipe:true}})
WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
```

   - Let's check and make sure it was successful

```
> db.cloud.find({name:"cloud02"})
{ "_id" : ObjectId("5c82b3660f767d000692acf7"), "notified" : true, "validated" : true, "released" : true, "name" : "cloud02", "description" : "EL7 to EL8 Satellite Upgrade", "owner" : "ikaur", "ticket" : "490957", "qinq" : 0, "wipe" : true, "ccuser" : [ "psuriset" ], "provisioned" : true }
```

   - Above, we can see this value was changed.
   - Lastly let's see if `quads-cli` thinks so too.

```
quads-cli --ls-wipe | grep cloud02
cloud02: True
```

* **Disclaimer** Generally you never need to modify things in MongoDB, there should be a `quads-cli` equivalent to do this safely and easily without mucking with the database.  If there's functionality missing here please [file a Github RFE](https://github.com/redhat-performance/quads/issues/new).

* Above, the correct way to adjust this is by redefining your cloud with all the same values but just not specify a wipe value.

```
quads-cli --define-cloud cloud02 --cloud-owner ikaur --force --description "EL7 to EL8 Satellite Upgrade" --cloud-ticket 490957 --cc-users "psuriset"
['Updated cloud cloud02']
```

* Note: if you **did not** want machines entering into a new environment to be wiped/provisioned just use define the environment with the `--no-wipe` option.

```
quads-cli --define-cloud cloud16 --cloud-owner jdoe --force --description "New Environment" --cloud-ticket 012345 --no-wipe
```

### Example: Querying Notification Values in MongoDB

* One more example: examining notification status of an assignment

   - We use ticket numbers as one of the metadata criteria to uniquely identify assignments
   - Here we'll query the notification status inside MongoDB for a particular workload.

```
> db.notification.find({ticket:"999999"})
{ "_id" : ObjectId("5ced1d769137063b1cadbc79"), "cloud" : ObjectId("5c82b36e0f767d000692ad0b"), "ticket" : "999999", "fail" : true, "success" : false, "initial" : false, "pre_initial" : true, "pre" : false, "one_day" : false, "three_days" : false, "five_days" : false, "seven_days" : false }
```

### Example: Query Multiple Values in MongoDB inside Collections

* Sometimes you want to drill down into multiple values in MongoDB, you can do this by passing multiple selection criteria.  In the following example we'll query for both a specific Cloud object ID and ticket number in the notification collection.

```
db.notification.find({cloud:ObjectId("5c82b3690f767d000692acff"), ticket: "491731"})
```

```
{ "_id" : ObjectId("5d03b161913706625477d581"), "cloud" : ObjectId("5c82b3690f767d000692acff"), "ticket" : "491731", "fail" : false, "success" : true, "initial" : true, "pre_initial" : true, "pre" : false, "one_day" : false, "three_days" : false, "five_days" : false, "seven_days" : false }
```

### Example: Manually Validate Hosts
* If there's systems you want to quickly pass through QUADS validation you can set `validated: true` in Mongo to release them.

* Check the `validated` flag

```
db.host.find({name: "f20-h01-000-5039ms.example.com"})
```

* Set `validated` to true.

```
db.host.update({name:"f20-h01-000-5039ms.example.com"}, {$set:{validated:true}})
```

* Re-running `/opt/quads/quads/tools/validate_env.py` should pass the systems.

### Example: Manually moving a Host Cloud in MongoDB

* Sometimes (hopefully rarely) you may need to move a host manually from one cloud to another, this is done by updating the `cloud:ObjectId` for the host object within MongoDB.

* Scenario: we need to move two hosts from cloud01 to cloud02, there's something wrong with our provisioning workflow and we've already verified the network switchports are changed, and the OS is provisioned.  We're going to move them manually.

```
quads-cli --move-hosts --dry-run
Moving f20-h01-000-r620.rdu2.example.com from cloud01 to cloud02, wipe = True
Moving f20-h14-000-r620.rdu2.example.com from cloud01 to cloud02, wipe = True
```

Above, we will move those two hosts manually inside MongoDB.

   - First, obtain the destination cloud ObjectID which is `5c82b3660f767d000692acf7`

```
> use quads
> db.cloud.find({name: "cloud02"})
{ "_id" : ObjectId("5c82b3660f767d000692acf7"), "notified" : true, "validated" : true, "released" : true, "name" : "cloud02", "description" : "EL7 to EL8 Satellite Upgrade", "owner" : "ikaur", "ticket" : "490957", "qinq" : 0, "wipe" : true, "ccuser" : [ "psuriset" ], "provisioned" : true }
```

   - Next, update the hosts document metadata within MongoDB to match the destination cloud.

```
db.host.find({name: "f20-h01-000-r620.rdu2.example.com"})
{ "_id" : ObjectId("5ce1e7e7913706568065a109"), "name" : "f20-h01-000-r620.rdu2.scalelab.example.com", "cloud" : ObjectId("5c82b3660f767d000692acf5"), "host_type" : "vendor", "interfaces" : [ { "name" : "em1", "mac_address" : "0c:c4:7a:eb:8b:a2", "ip_address" : "10.1.34.233", "switch_port" : "xe-0/0/0:0" }, { "name" : "em2", "mac_address" : "0c:c4:7a:eb:8b:a3", "ip_address" : "10.1.34.233", "switch_port" : "xe-0/0/0:1" }, { "name" : "em3", "mac_address" : "b8:ca:3a:61:41:68", "ip_address" : "10.1.34.233", "switch_port" : "xe-0/0/8:0" }, { "name" : "em4", "mac_address" : "b8:ca:3a:61:41:6a", "ip_address" : "10.1.34.233", "switch_port" : "xe-0/0/8:1" } ], "nullos" : true, "build" : false
```

   - We see that the current Cloud ObjectID is `5c82b3660f767d000692acf5` for cloud01, we need it to be `5c82b3660f767d000692acf7`


```
db.host.update({name:"f20-h01-000-r620.rdu2.example.com"}, {$set:{cloud:ObjectId("5c82b3660f767d000692acf7")}})
db.host.update({name:"f20-h14-000-r620.rdu2.example.com"}, {$set:{cloud:ObjectId("5c82b3660f767d000692acf7")}})
```

   - Now `--move-hosts --dry-run` will believe these hosts have already moved.  All done.


```
quads-cli --move-hosts --dry-run
Nothing to do.
```

### Example: Toggling Individual Cloud Metadata Settings

If you really need to manually toggle individual cloud metadata settings this is possible as well, in this example we'll toggle the `validated` flag.

```
db.cloud.update({name:"cloud21"}, {$set:{validated:true}})
```

### Example: Modifying cc-users

If a future cloud is defined and scheduled with future hosts you will currently not be able to redefine it with `--define-cloud --force` to either append or remove `cc-users`.  To do this in MongoDB you can adjust it like so:

```
db.cloud.update({name:"cloud07"}, {$set:{ccuser:["kreeves", "gcarlin", "bmurray", "mhedberg"]}})
```
