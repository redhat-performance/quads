#!/usr/bin/env bash

# curl -k -X POST -u "grafuls@redhat.com:password" -H "Content-Type: application/json" http://127.0.0.1:5000/api/v3/login/

export TOKEN=$(sed -e 's/^"//' -e 's/"$//' <<< $(curl -k -X POST -u "grafuls@redhat.com:password" -H "Content-Type: application/json" http://127.0.0.1:5000/api/v3/login/ | awk -F\: '{print $2}' | awk -F\, '{print $1}'))

curl -k -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"name":"cloud01"}' http://127.0.0.1:5000/api/v3/clouds/

curl -k -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"name":"cloud02"}' http://127.0.0.1:5000/api/v3/clouds/

curl -k -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"name":"cloud03"}' http://127.0.0.1:5000/api/v3/clouds/

curl -k -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"name":"cloud04"}' http://127.0.0.1:5000/api/v3/clouds/

curl -k -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"name":"cloud05"}' http://127.0.0.1:5000/api/v3/clouds/

curl -k -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"name":"cloud06"}' http://127.0.0.1:5000/api/v3/clouds/

curl -k -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"name":"cloud07"}' http://127.0.0.1:5000/api/v3/clouds/

curl -k -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"name":"host1.example.com", "default_cloud":"cloud01", "model": "fc640", "host_type": "scalelab"}' http://127.0.0.1:5000/api/v3/hosts/

curl -k -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"name":"host2.example.com", "default_cloud":"cloud01", "model": "r640", "host_type": "scalelab"}' http://127.0.0.1:5000/api/v3/hosts/

curl -k -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"name":"host3.example.com", "default_cloud":"cloud01", "model": "1029p", "host_type": "scalelab"}' http://127.0.0.1:5000/api/v3/hosts/

curl -k -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"disk_type":"nvme","size_gb":2000, "count":2}' http://127.0.0.1:5000/api/v3/disks/host1.example.com

curl -k -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"disk_type":"nvme","size_gb":2000, "count":2}' http://127.0.0.1:5000/api/v3/disks/host2.example.com

curl -k -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"disk_type":"scsi","size_gb":1000, "count":2}' http://127.0.0.1:5000/api/v3/disks/host3.example.com

curl -k -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"name":"em1", "bios_id":"NIC.Integrated.1", "mac_address": "00:d3:00:e4:00:c2", "switch_ip":"192.168.1.2", "switch_port":"et-0/0/0:1", "speed":1000, "vendor":"Mellanox"}' http://127.0.0.1:5000/api/v3/interfaces/host1.example.com

curl -k -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"name":"em1", "bios_id":"NIC.Integrated.1", "mac_address": "00:d3:00:e4:00:c3", "switch_ip":"192.168.1.2", "switch_port":"et-0/0/0:2", "speed":1000, "vendor":"Mellanox"}' http://127.0.0.1:5000/api/v3/interfaces/host2.example.com

curl -k -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"name":"em1", "bios_id":"NIC.Integrated.1", "mac_address": "00:d3:00:e4:00:c4", "switch_ip":"192.168.1.2", "switch_port":"et-0/0/0:3", "speed":1000, "vendor":"Mellanox"}' http://127.0.0.1:5000/api/v3/interfaces/host3.example.com

curl -k -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"handle":"DIMM1", "size_gb":2000}' http://127.0.0.1:5000/api/v3/memory/host1.example.com

curl -k -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"handle":"DIMM2", "size_gb":2000}' http://127.0.0.1:5000/api/v3/memory/host1.example.com

curl -k -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"handle":"DIMM1", "size_gb":2000}' http://127.0.0.1:5000/api/v3/memory/host2.example.com

curl -k -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"handle":"DIMM2", "size_gb":1000}' http://127.0.0.1:5000/api/v3/memory/host2.example.com

curl -k -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"handle":"DIMM1", "size_gb":1000}' http://127.0.0.1:5000/api/v3/memory/host3.example.com


curl -k -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"handle":"Intel-i7", "vendor":"Intel", "product":"i7","cores":12,"threads":24}' http://127.0.0.1:5000/api/v3/processors/host1.example.com

curl -k -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"handle":"Raizen", "vendor":"AMD", "product":"raizen","cores":10,"threads":20}' http://127.0.0.1:5000/api/v3/processors/host2.example.com

curl -k -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"handle":"Raizen", "vendor":"AMD", "product":"raizen","cores":10,"threads":20}' http://127.0.0.1:5000/api/v3/processors/host3.example.com

curl -k -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"gateway":"192.168.12.19", "ip_free":510,"ip_range":"10.1.48.0/23", "netmask":"255.255.0.0","vlan_id":"601"}' http://127.0.0.1:5000/api/v3/vlans/

curl -k -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"cloud":"cloud02","vlan":"601","description":"Test allocation","owner":"grafuls","ticket":"123","cc_user":"gonza"}' http://127.0.0.1:5000/api/v3/assignments/

curl -k -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"cloud":"cloud02", "host":"host2.example.com", "start":"2023-02-28 22:00", "end":"2023-03-02 22:00"}' http://127.0.0.1:5000/api/v3/schedules/
