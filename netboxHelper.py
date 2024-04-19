import utils


# used in syncSites and syncDevices
def get_sites_nb_dict(nb):
    return [
        {
            "id": site_nb.id,
            "name": site_nb.name,
            "slug": site_nb.slug,
            "status": site_nb.status,
            "facility": site_nb.facility,
            "physical_address": site_nb.physical_address,
            "shipping_address": site_nb.shipping_address,
            "latitude": site_nb.latitude,
            "longitude": site_nb.longitude,
        }
        for site_nb in nb.dcim.sites.all()
    ]


# used in syncOrgs and syncSites and syncDevices
def get_site_groups_info(nb):
    return [
        {
            "id": site_group_nb.id,
            "org_key": site_group_nb.description,
            "name": site_group_nb.name,
        }
        for site_group_nb in nb.dcim.site_groups.all()
    ]




def get_device_types_dict(nb):
    
    return [
        {
            "id": device_type.id,
            "manufacturer": device_type.manufacturer,
            "part_number": device_type.part_number,
            "model": device_type.model,
            "role": (
                device_type.custom_fields["role"]["id"]
                if device_type.custom_fields["role"] is not None
                else None
            ),
        }
        for device_type in nb.dcim.device_types.all()
    ]


def get_devices_dict_for_site(site_id, nb):
    devices_nb = nb.dcim.devices.filter(site_id=site_id)
    devices_nb_dict = []
    if devices_nb:
        for device_nb in devices_nb:
            devices_nb_dict.append(
                {
                    "id": device_nb.id,
                    "name": device_nb.name,
                    "device_role": device_nb.role,
                    "device_type": device_nb.device_type,
                    "serial_number": device_nb.serial,
                    "asset_tag": device_nb.asset_tag,
                    "status": device_nb.status,
                    "site": device_nb.site,
                    "asset_url": device_nb.custom_fields["asset_url"],
                    "firmware": device_nb.custom_fields["firmware"],
                    "floor_id": device_nb.custom_fields["floor_id"],
                    "lan_ip": device_nb.custom_fields["lan_ip"],

                    "tags": device_nb.custom_fields["tags"],
                    "wan_primary_ip": device_nb.custom_fields["wan_primary_ip"],
                    "wan_secondary_ip": device_nb.custom_fields["wan_secondary_ip"],
                    "wireless_mac": device_nb.custom_fields["wireless_mac"],
                }
            )
    return devices_nb_dict
