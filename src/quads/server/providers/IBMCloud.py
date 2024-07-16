from quads.server.providers.base import Provider
from quads.config import Config


import SoftLayer


class IBMCloud(Provider):
    def __init__(self):
        super().__init__()
        self.username = Config.get("ibm_cloud_username")
        self.api_key = Config.get("ibm_cloud_api_key")
        self.client = SoftLayer.create_client_from_env(username=self.username, api_key=self.api_key)
        self.hw_manager = SoftLayer.HardwareManager(self.client)

    def get_hardware_id(self, hostname):
        """Get hardware_id by hostname short FQDN"""
        hw_id = self.hw_manager.resolve_ids(hostname)
        return hw_id[0]

    def create(self, hostname, ssh_keys, no_public):
        """Create new bare metal instance."""
        self.hw_manager.place_order(
            hostname=hostname,
            domain="performance-scale.cloud",
            location="dal10",
            os="OS_RHEL_8_X_64_BIT_PER_PROCESSOR_LICENSING",
            port_speed="100_MBPS_PUBLIC_PRIVATE_NETWORK_UPLINKS",
            ssh_keys=ssh_keys,
            hourly=False,
            no_public=no_public,
        )
        hardware_id = self.get_hardware_id(hostname)
        result = self.hw_manager.wait_for_ready(hardware_id)
        return result

    def cancel(self, hostname):
        """Terminate a bare metal instance"""
        hardware_id = self.get_hardware_id(hostname)
        result = self.hw_manager.cancel_hardware(hardware_id=hardware_id)
        return result

    def edit(self, hardware_id, **kwargs):
        """Edit hostname, domain name, notes, user data of the hardware."""
        result = self.hw_manager.edit(hardware_id=hardware_id, **kwargs)
        return result

    def list_hardware(self):
        """List all hardware associated with the authenticated account"""
        object_mask = "mask[hostname,id]"
        hw_list = self.hw_manager.list_hardware(mask=object_mask)
        return hw_list
