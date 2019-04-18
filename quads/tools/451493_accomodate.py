from quads.model import Notification, Cloud, Vlan

if __name__ == "__main__":
    clouds = Cloud.objects()
    for cloud in clouds:
        # Insert notification doc for all clouds
        Notification(cloud=cloud, ticket=cloud.ticket).save()
        if cloud.ticket != "000000":
            # Add provisioned field to all clouds
            cloud.update(provisioned=cloud.released)

    vlans = Vlan.objects()
    for vlan in vlans:
        # Ticket to string field on VLAN doc
        vlan.update(ticket="000000")
