#!/usr/bin/python3
"""
Temporary script to accommodate to non backwards compatible changes
"""

from quads.model import Notification, Cloud, Vlan

if __name__ == "__main__":
    clouds = Cloud.objects()
    for cloud in clouds:
        # Insert notification doc for all clouds
        Notification(
            cloud=cloud,
            ticket=cloud.ticket,
            fail=False,
            success=True,
            initial=True,
            pre_initial=True,
            pre=True,
            one_day=True,
            three_days=True,
            five_days=True,
            seven_days=True
        ).save()
        # Add provisioned field to all clouds
        cloud.update(provisioned=cloud.released)

    vlans = Vlan.objects()
    for vlan in vlans:
        # Ticket to string field on VLAN doc
        vlan.update(ticket=str(vlan.ticket))
