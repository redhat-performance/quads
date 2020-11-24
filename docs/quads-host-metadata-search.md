QUADS Metadata Model and Search Library
======================================

In QUADS `1.1.4` and above we've implemented a metadata model in MongoDB that captures information about host hardware, model, and other useful information.  We'll be expanding this as time progresses.

![quads](../image/quads.jpg?raw=true)

  * [How to Import Host Metadata](#how-to-import-host-metadata)
    * [Modify YAML Host Data](#modify-yaml-host-data)
    * [Add any Supporting Model Type](#add-any-supporting-model-type)
    * [Importing Host Metadata](#importing-host-metadata)
  * [How to Export Host Metadata](#how-to-export-host-metadata)
  * [Querying Host Information](#querying-host-information)
    * [Example Filter Searches](#example-filter-searches)

## How to Import Host Metadata
### Modify YAML Host Data
  * Host metadata uses a standard YAML key/value pair format, here's a [reference example](../conf/hosts_metadata.yml)
  * Host metadata is not required unless you want to use it, **it is entirely optional**

### Add any Supporting Model Type
  * We list some example model types of baremetal systems we use, you will also want to edit the `models:` value so it has any additional system models you might use in the [QUADS Conf](../conf/hosts_metadata.yml#L238)
  * To generate a YAML metadata file for importing QUADS-managed hosts you can use this command:

```
for h in $(quads-cli --ls-hosts) ; do echo "- name: $h" ; echo "  model: $(echo $h | awk -F. '{ print $1 }' | awk -F- '{ print $NF }' | tr a-z A-Z)" ; done > /tmp/hosts_metadata.yml
```

### Importing Host Metadata

  * To import host metadata from a file:

```
quads-cli --define-host-details --metadata /tmp/hosts_metadata.yml
```

  * Doing this again or modifying your `hosts_metadata.yml` file and re-importing will overwrite all values or remove ones that might have been removed from the QUADS database.

## How to Export Host Metadata
  * To export the same formatted YAML key/value pair metadata data source from your hosts use the `--export-host-details` command.
  * The file provided should be a new file, or overwrite an existing one and the path should be somewhere on the filesystem.

```
quads-cli --export-host-details /tmp/my_host_data.yml
```

## Querying Host Information
  * A new sub-command of `--filter` has been added to the `--ls-available` and `--ls-hosts` commands.

| Component        | Field Type | Syntax          | Operators       |
|------------------|------------|-----------------|-----------------|
| model            |  string    | exact match     | ==,!=           |
| disks.size_gb    |  integer   | disk size in GB | ==,!=,<,<=,>,>= |
| disks.disks_type |  string    | nvme,sata,ssd   | ==,!=           |
| disks.count      |  integer   | number of disks | ==,!=,<,<=,>,>= |


### Example Filter Searches
  * Accepted operators are `==, !=, <, <=, >, >=`

  * Search for systems with disk type NVMe, with a size of 2TB or more and available between `2020-07-20 17:00` and `2020-07-22 13:00`

```
quads-cli --ls-available --schedule-start "2020-07-20 17:00" --schedule-end "2020-07-22 13:00" --filter "disks.disk_type==nvme,disks.size_gb>=2000"
```

  * Search for systems with SATA disks available from `2020-07-20 17:00` until `2020-07-22 13:00`

```
quads-cli --ls-available --schedule-start "2020-07-20 17:00" --schedule-end "2020-07-22 13:00" --filter "disks.disk_type==sata"
```

  * Search for systems of model type `1029U-TRTP` available from `2020-07-20 17:00` until `2020-07-22 13:00`

```
quads-cli --ls-available --schedule-start "2020-07-20 17:00" --schedule-end "2020-07-22 13:00" --filter "model==1029U-TRTP"
```

  * Search for systems with **two NVMe** disks **and** disk size of **more than** 2TB, available from `2020-07-20 17:00` until `2020-07-22 13:00`

```
quads-cli --ls-available --schedule-start "2020-07-20 17:00" --schedule-end "2020-07-22 13:00" --filter "disks.disk_type==nvme,disks.count>2, disks.size_gb<2000"
```

  * Search all systems by MAC Address.
  * This is useful for finding what host has what MAC Address.

```
quads-cli --ls-hosts --filter "interfaces.mac_address==ac:1f:6b:2d:19:48"
```

  * Search all systems by model and number of interfaces.

```
quads-cli --ls-hosts --filter "model==FC640,interfaces__size==5"
```
