QUADS Metadata Model and Search Library
======================================

In QUADS `1.1.4` and above we've implemented a metadata model in MongoDB that captures information about host hardware, model, and other useful information.  We'll be expanding this as time progresses.

![quads](../image/quads.jpg?raw=true)

  * [How to Import Host Metadata](#how-to-import-host-metadata)
  * [How to Export Host Metadata](#how-to-export-host-metadata)
  * [Querying Host Information](#querying-host-information)
    * [Example Filter Searches](#example-filter-searches)

## How to Import Host Metadata
  * Host metadata uses a standard YAML key/value pair format, here's a [reference example](../conf/hosts_metadata.yml)
  * We'll be providing a tool later to automatically interrogate and generate this for you across all or some subset of hosts.
  * Host metadata is not required unless you want to use it, it is entirely optional.
  * To import host metadata:

```
quads-cli --define-host-details --metadata conf/hosts_metadata.yml
```

## How to Export Host Metadata
  * To export the same formatted YAML key/value pair metadata data source from your hosts use the `--export-host-details` command.
  * The file provided should be a new file, or overwrite an existing one and the path should be somewhere on the filesystem.

```
quads-cli --export-host-details /tmp/my_host_data.yml
```

## Querying Host Information
  * A new sub-command of `--filter` has been added to the `--ls-available`
  * While not yet in place, we'll also expand this to `--ls-hosts` as well in the future.

### Example Filter Searches
  * Accepted operators are `==, !=, <, <=, >, >=`

  * Search for systems with disk type NVMe, with a size of 2TB or more and available between `2020-07-20 17:00` and `2020-07-22 13:00`

```
quads-cli --ls-available --schedule-start "2020-07-20 17:00" --schedule-end "2020-07-22 13:00" --filter "disks.disk_type==nvme,disks.size_gb>2000"
```

  * Search for systems with SATA disks available from `2020-07-20 17:00` until `2020-07-22 13:00`

```
quads-cli --ls-available --schedule-start "2020-07-20 17:00" --schedule-end "2020-07-22 13:00" --filter "disks.disk_type==sata"
```

  * Search for systems of model type `1029U-TRTP` available from `2020-07-20 17:00` until `2020-07-22 13:00`

```
quads-cli --ls-available --schedule-start "2020-07-20 17:00" --schedule-end "2020-07-22 13:00" --filter "model=1029U-TRTP"
```

  * Search for systems with **two NVMe** disks **and** disk size of **more than** 2TB, available from `2020-07-20 17:00` until `2020-07-22 13:00`

```
quads-cli --ls-available --schedule-start "2020-07-20 17:00" --schedule-end "2020-07-22 13:00" --filter "disks.disk_type==nvme,disks.count>2, disks.size_gb<2000"
```
