"""Template responses and requests for API testing."""
# --------------------
# AUTH
# --------------------
EXPIRED_TEST_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NzU3Njc4NDUsImlhdCI6MTY3NTc2MTg0NSwic3ViIjoi" \
                     "Z3JhZnVsc0ByZWRoYXQuY29tIn0.lDTmUpY4b3sICYUcAriui6yTv-iki10fBm07x6fuayc"

# --------------------
# HOSTS
# --------------------
HOST_1_REQUEST = {"name": "host1.example.com", "default_cloud": "cloud01", "model": "fc640", "host_type": "scalelab"}
HOST_2_REQUEST = {"name": "host2.example.com", "default_cloud": "cloud01", "cloud": "cloud02",
                  "model": "r640", "host_type": "scalelab"}
HOST_3_REQUEST = {"name": "host3.example.com", "default_cloud": "cloud01", "model": "1029p", "host_type": "scalelab"}
HOST_4_REQUEST = {"name": "host4.example.com", "default_cloud": "cloud01", "model": "r640",
                  "cloud": "cloud03", "host_type": "scalelab"}
HOST_5_REQUEST = {"name": "host5.example.com", "default_cloud": "cloud01", "model": "6048r",
                  "cloud": "cloud05", "host_type": "scalelab"}

# --------------------
# DISKS
# --------------------
DISK_1_REQUEST = ({"disk_type": "nvme", "size_gb": 2000, "count": 2}, "host1.example.com")
DISK_1_RESPONSE = {"disk_type": "nvme", "size_gb": 2000, "count": 2, "host_id": 1, "id": 1}
DISK_2_REQUEST = ({"disk_type": "sata", "size_gb": 4000, "count": 1}, "host1.example.com")
DISK_2_RESPONSE = {"disk_type": "sata", "size_gb": 4000, "count": 1, "host_id": 1, "id": 2}
DISK_3_REQUEST = ({"disk_type": "nvme", "size_gb": 1000, "count": 3}, "host2.example.com")
DISK_4_REQUEST = ({"disk_type": "scsi", "size_gb": 1000, "count": 2}, "host3.example.com")

# --------------------
# INTERFACES
# --------------------
INTERFACE_1_REQUEST = ({
                           "name": "em1",
                           "bios_id": "NIC.Integrated.1",
                           "mac_address": "00:d3:00:e4:00:c2",
                           "switch_ip": "192.168.1.2",
                           "switch_port": "et-0/0/0:1",
                           "speed": 1000,
                           "vendor": "Mellanox"
                       }, "host1.example.com")
INTERFACE_1_RESPONSE = {
    "name": "em1",
    "bios_id": "NIC.Integrated.1",
    "mac_address": "00:d3:00:e4:00:c2",
    "switch_ip": "192.168.1.2",
    "switch_port": "et-0/0/0:1",
    "speed": 1000,
    "vendor": "Mellanox",
    "host_id": 1,
    "id": 1,
    "maintenance": False,
    "pxe_boot": False
}
INTERFACE_1_UPDATE_REQUEST = {
    "id": 1,
    "switch_ip": "192.168.2.2",
    "switch_port": "et-0/0/0:2"
}
INTERFACE_1_UPDATE_RESPONSE = {
    key: INTERFACE_1_UPDATE_REQUEST.get(key, INTERFACE_1_RESPONSE[key])
    for key
    in INTERFACE_1_RESPONSE
}
INTERFACE_2_REQUEST = ({
                           "name": "em1",
                           "bios_id": "NIC.Integrated.1",
                           "mac_address": "00:d3:00:e4:00:c3",
                           "switch_ip": "192.168.1.2",
                           "switch_port": "et-0/0/0:2",
                           "speed": 1000,
                           "vendor": "Mellanox"
                       }, "host2.example.com")
INTERFACE_3_REQUEST = ({
                           "name": "em1",
                           "bios_id": "NIC.Integrated.1",
                           "mac_address": "00:d3:00:e4:00:c2",
                           "switch_ip": "192.168.1.2",
                           "switch_port": "et-0/0/0:3",
                           "speed": 10000,
                           "vendor": "Mellanox"
                       }, "host3.example.com")
INTERFACE_4_REQUEST = ({
                           "name": "em1",
                           "bios_id": "NIC.Integrated.1",
                           "mac_address": "00:d3:00:e4:00:c5",
                           "switch_ip": "192.168.2.2",
                           "switch_port": "et-0/0/0:1",
                           "speed": 1000,
                           "vendor": "Mellanox"
                       }, "host4.example.com")

# --------------------
# MEMORY
# --------------------
MEMORY_1_REQUEST = ({"handle": "DIMM1", "size_gb": 2}, "host1.example.com")
MEMORY_1_RESPONSE = {"handle": "DIMM1", "size_gb": 2, "host_id": 1, "id": 1}
MEMORY_2_REQUEST = ({"handle": "DIMM2", "size_gb": 2}, "host1.example.com")
MEMORY_2_RESPONSE = {"handle": "DIMM2", "size_gb": 2, "host_id": 1, "id": 3}
MEMORY_3_REQUEST = ({"handle": "DIMM1", "size_gb": 4}, "host2.example.com")
MEMORY_3_RESPONSE = {"handle": "DIMM1", "size_gb": 4, "host_id": 2, "id": 2}
MEMORY_4_REQUEST = ({"handle": "DIMM1", "size_gb": 2}, "host2.example.com")
MEMORY_5_REQUEST = ({"handle": "DIMM1", "size_gb": 16}, "host3.example.com")
MEMORY_6_REQUEST = ({"handle": "DIMM2", "size_gb": 8}, "host4.example.com")

# --------------------
# PROCESSORS
# --------------------
PROCESSOR_1_REQUEST = ({
                           "handle": "Intel Xeon Gold 6230 - 1",
                           "vendor": "Intel",
                           "product": "Xeon Gold 6230",
                           "cores": 20,
                           "threads": 40
                       }, "host1.example.com")
PROCESSOR_1_RESPONSE = {
    "handle": "Intel Xeon Gold 6230 - 1",
    "vendor": "Intel",
    "product": "Xeon Gold 6230",
    "cores": 20,
    "threads": 40,
    "host_id": 1,
    "id": 1
}
PROCESSOR_2_REQUEST = ({
                           "handle": "Intel Xeon Gold 6230 - 2",
                           "vendor": "Intel",
                           "product": "Xeon Gold 6230",
                           "cores": 20,
                           "threads": 40
                       }, "host1.example.com")
PROCESSOR_2_RESPONSE = {
    "handle": "Intel Xeon Gold 6230 - 2",
    "vendor": "Intel",
    "product": "Xeon Gold 6230",
    "cores": 20,
    "threads": 40,
    "host_id": 1,
    "id": 2
}
PROCESSOR_3_REQUEST = ({
                           "handle": "Intel Xeon Gold 6330 - 1",
                           "vendor": "Intel",
                           "product": "Xeon Gold 6330",
                           "cores": 28,
                           "threads": 56
                       }, "host2.example.com")
PROCESSOR_4_REQUEST = ({
                           "handle": "AMD EPYC 7742 - 1",
                           "vendor": "AMD",
                           "product": "EPYC 7742",
                           "cores": 64,
                           "threads": 128
                       }, "host3.example.com")
PROCESSOR_5_REQUEST = ({
                           "handle": "Intel Xeon Gold 6230 - 1",
                           "vendor": "Intel",
                           "product": "Xeon Gold 6230",
                           "cores": 20,
                           "threads": 40
                       }, "host4.example.com")

# --------------------
# VLANs
# --------------------
VLAN_1_REQUEST = {
    "gateway": "192.168.12.19",
    "ip_free": 510,
    "ip_range": "10.1.48.0/23",
    "netmask": "255.255.0.0",
    "vlan_id": 601
}
VLAN_1_RESPONSE = {
    "gateway": "192.168.12.19",
    "ip_free": 510,
    "ip_range": "10.1.48.0/23",
    "netmask": "255.255.0.0",
    "vlan_id": 601,
    "id": 1
}
VLAN_2_REQUEST = {
    "gateway": "192.168.12.20",
    "ip_free": 1022,
    "ip_range": "10.1.50.0/22",
    "netmask": "255.255.252.0",
    "vlan_id": 602
}
VLAN_2_RESPONSE = {
    "gateway": "192.168.12.20",
    "ip_free": 1022,
    "ip_range": "10.1.50.0/22",
    "netmask": "255.255.252.0",
    "vlan_id": 602,
    "id": 2
}
VLAN_3_REQUEST = {
    "gateway": "192.168.12.21",
    "ip_free": 1022,
    "ip_range": "10.1.54.0/22",
    "netmask": "255.255.252.0",
    "vlan_id": 603
}

# --------------------
# ASSIGNMENTS
# --------------------
ASSIGNMENT_1_REQUEST = {
    "cloud": "cloud02",
    "vlan": "601",
    "description": "Test allocation.",
    "owner": "grafuls",
    "ticket": "1",
    "cc_user": "gonza"
}
ASSIGNMENT_1_RESPONSE = {
    "active": True,
    "ccuser": ["gonza"],
    "cloud": {
        "id": 2,
        "last_redefined": "___",
        "name": "cloud02"
    },
    "cloud_id": 2,
    "created_at": "___",
    "description": "Test allocation.",
    "id": 1,
    "notification": {
        "assignment_id": 1,
        "fail": False,
        "five_days": False,
        "id": 1,
        "initial": False,
        "one_day": False,
        "pre": False,
        "pre_initial": False,
        "seven_days": False,
        "success": False,
        "three_days": False
    },
    "owner": "grafuls",
    "provisioned": False,
    "qinq": None,
    "ticket": "1",
    "validated": False,
    "vlan": {
        "gateway": "192.168.12.19",
        "id": 1,
        "ip_free": 510,
        "ip_range": "10.1.48.0/23",
        "netmask": "255.255.0.0",
        "vlan_id": 601
    },
    "vlan_id": 1,
    "wipe": False
}
ASSIGNMENT_1_UPDATE_REQUEST = {
    "cloud": "cloud04",
    "vlan": "603",
    "description": "Updated description.",
    "owner": "gonza",
    "ticket": "123",
    "qinq": "1",
    "wipe": "True",
    "ccuser": "gonza, grafuls"
}
ASSIGNMENT_1_UPDATE_RESPONSE = {
    "active": True,
    "ccuser": ["gonza", "grafuls"],
    "cloud": {
        "id": 4,
        "last_redefined": "___",
        "name": "cloud04"
    },
    "cloud_id": 4,
    "created_at": "___",
    "description": "Updated description.",
    "id": 1,
    "notification": {
        "assignment_id": 1,
        "fail": False,
        "five_days": False,
        "id": 1,
        "initial": False,
        "one_day": False,
        "pre": False,
        "pre_initial": False,
        "seven_days": False,
        "success": False,
        "three_days": False
    },
    "owner": "gonza",
    "provisioned": False,
    "qinq": 1,
    "ticket": "123",
    "validated": False,
    "vlan": {
        "gateway": "192.168.12.21",
        "id": 3,
        "ip_free": 1022,
        "ip_range": "10.1.54.0/22",
        "netmask": "255.255.252.0",
        "vlan_id": 603
    },
    "vlan_id": 3,
    "wipe": True
}
ASSIGNMENT_2_REQUEST = {
    "cloud": "cloud03",
    "vlan": "602",
    "description": "Test allocation.",
    "owner": "grafuls",
    "ticket": "2",
    "cc_user": "gonza"
}
ASSIGNMENT_2_RESPONSE = {
    'active': True,
    'ccuser': ['gonza'],
    'cloud': {
        'id': 3,
        'last_redefined': '___',
        'name': 'cloud03'},
    'cloud_id': 3,
    'created_at': '___',
    'description': 'Test allocation.',
    'id': 2,
    'notification': {
        'assignment_id': 2,
        'fail': False,
        'five_days': False,
        'id': 2,
        'initial': False,
        'one_day': False,
        'pre': False,
        'pre_initial': False,
        'seven_days': False,
        'success': False,
        'three_days': False
    },
    'owner': 'grafuls',
    'provisioned': False,
    'qinq': None,
    'ticket': '2',
    'validated': False,
    'vlan': {
        'gateway': '192.168.12.20',
        'id': 2,
        'ip_free': 1022,
        'ip_range': '10.1.50.0/22',
        'netmask': '255.255.252.0',
        'vlan_id': 602
    },
    'vlan_id': 2,
    'wipe': False
}

# --------------------
# SCHEDULES
# --------------------
SCHEDULE_1_REQUEST = {
    "cloud": "cloud02",
    "hostname": "host2.example.com",
    "start": "2023-02-04 22:00",
    "end": "2042-03-18 22:00",
}
SCHEDULE_1_RESPONSE = {
    'assignment': {
        'active': True,
        'ccuser': ['gonza'],
        'cloud': {
            'id': 2,
            'last_redefined': 'Tue, 07 Mar 2023 11:36:53 GMT',
            'name': 'cloud02'
        },
        'cloud_id': 2,
        'created_at': 'Tue, 07 Mar 2023 11:36:53 GMT',
        'description': 'Test allocation.',
        'id': 1,
        'notification': {
            'assignment_id': 1,
            'fail': False,
            'five_days': False,
            'id': 1,
            'initial': False,
            'one_day': False,
            'pre': False,
            'pre_initial': False,
            'seven_days': False,
            'success': False,
            'three_days': False
        },
        'owner': 'grafuls',
        'provisioned': False,
        'qinq': None,
        'ticket': '1',
        'validated': False,
        'vlan': {
            'gateway': '192.168.12.19',
            'id': 1,
            'ip_free': 510,
            'ip_range': '10.1.48.0/23',
            'netmask': '255.255.0.0',
            'vlan_id': 601
        },
        'vlan_id': 1,
        'wipe': False
    },
    'assignment_id': 1,
    'build_end': None,
    'build_start': None,
    'created_at': 'Tue, 07 Mar 2023 11:36:53 GMT',
    'end': 'Tue, 18 Mar 2042 22:00:00 GMT',
    'host': {
        'broken': False,
        'build': False,
        'cloud': {
            'id': 2,
            'last_redefined': 'Tue, 07 Mar 2023 11:36:53 GMT',
            'name': 'cloud02'
        },
        'cloud_id': 2,
        'created_at': 'Tue, 07 Mar 2023 11:36:53 GMT',
        'default_cloud': {
            'id': 1,
            'last_redefined': 'Tue, 07 Mar 2023 11:36:53 GMT',
            'name': 'cloud01'
        },
        'default_cloud_id': 1,
        'host_type': 'scalelab',
        'id': 2,
        'last_build': None,
        'model': 'R640',
        'name': 'host2.example.com',
        'retired': False,
        'switch_config_applied': False,
        'validated': False
    },
    'host_id': 2,
    'id': 1,
    'index': None,
    'start': 'Sat, 04 Feb 2023 22:00:00 GMT'
}
SCHEDULE_2_REQUEST = {
    "cloud": "cloud03",
    "hostname": "host3.example.com",
    "start": "2023-02-04 22:00",
    "end": "2044-03-18 22:00",
}
SCHEDULE_2_RESPONSE = {
    'assignment': {
        'active': True,
        'ccuser': ['gonza'],
        'cloud': {
            'id': 3,
            'last_redefined': 'Tue, 07 Mar 2023 11:36:53 GMT',
            'name': 'cloud03'
        },
        'cloud_id': 3,
        'created_at': 'Tue, 07 Mar 2023 11:36:53 GMT',
        'description': 'Test allocation.',
        'id': 2,
        'notification': {
            'assignment_id': 2,
            'fail': False,
            'five_days': False,
            'id': 2,
            'initial': False,
            'one_day': False,
            'pre': False,
            'pre_initial': False,
            'seven_days': False,
            'success': False,
            'three_days': False
        },
        'owner': 'grafuls',
        'provisioned': False,
        'qinq': None,
        'ticket': '2',
        'validated': False,
        'vlan': {
            'gateway': '192.168.12.20',
            'id': 2,
            'ip_free': 1022,
            'ip_range': '10.1.50.0/22',
            'netmask': '255.255.252.0',
            'vlan_id': 602
        },
        'vlan_id': 2,
        'wipe': False
    },
    'assignment_id': 2,
    'build_end': None,
    'build_start': None,
    'created_at': 'Tue, 07 Mar 2023 11:36:53 GMT',
    'end': 'Fri, 18 Mar 2044 22:00:00 GMT',
    'host': {
        'broken': False,
        'build': False,
        'cloud': {
            'id': 1,
            'last_redefined': 'Tue, 07 Mar 2023 11:36:53 GMT',
            'name': 'cloud01'
        },
        'cloud_id': 1,
        'created_at': 'Tue, 07 Mar 2023 11:36:53 GMT',
        'default_cloud': {
            'id': 1,
            'last_redefined': 'Tue, 07 Mar 2023 11:36:53 GMT',
            'name': 'cloud01'
        },
        'default_cloud_id': 1,
        'host_type': 'scalelab',
        'id': 3,
        'last_build': None,
        'model': '1029P',
        'name': 'host3.example.com',
        'retired': False,
        'switch_config_applied': False,
        'validated': False
    },
    'host_id': 3,
    'id': 2,
    'index': None,
    'start': 'Sat, 04 Feb 2023 22:00:00 GMT'
}
SCHEDULE_1_UPDATE_REQUEST = {
    "start": "2023-02-04 22:00",
    "end": "2032-02-04 22:00",
    "build_start": "2024-02-04 22:00",
    "build_end": "2024-02-05 22:00",
}
