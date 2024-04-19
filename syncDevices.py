import json
import utils
import netboxHelper
import merakiHelper

meraki_api_key, netbox_api_key, netbox_url = utils.setup_environment()
nb = utils.setup_netbox_client(netbox_url, netbox_api_key)
dashboard = utils.setup_meraki_client()

sites_nb_dict = netboxHelper.get_sites_nb_dict(nb)
device_types_dict = netboxHelper.get_device_types_dict(nb)

for site_nb in sites_nb_dict:
    print("Site: ", site_nb["name"], "Facility: ", site_nb["facility"])

    devices_nb_dict = netboxHelper.get_devices_dict_for_site(site_nb["id"], nb)
    devices_mrk_dict = merakiHelper.get_devices_mrk_dict(site_nb["facility"], device_types_dict, dashboard)

    devices_nb_by_asset_tag = {device["asset_tag"].strip(): device for device in devices_nb_dict}
    devices_nb_by_name = {device["name"].strip(): device for device in devices_nb_dict}

    devices_mrk_by_asset_tag = {device["asset_tag"].strip(): device for device in devices_mrk_dict}
    devices_mrk_by_name = {device["name"].strip(): device for device in devices_mrk_dict}

    asset_tags_nb = set(devices_nb_by_asset_tag.keys())
    asset_tags_mrk = set(devices_mrk_by_asset_tag.keys())
    names_nb = set(devices_nb_by_name.keys())
    names_mrk = set(devices_mrk_by_name.keys())

    devices_to_update = []

    for asset_tag in asset_tags_nb.intersection(asset_tags_mrk):
        nb_device = devices_nb_by_asset_tag[asset_tag]
        mrk_device = devices_mrk_by_asset_tag[asset_tag]

        if (
            nb_device.get("asset_url") != mrk_device.get("asset_url")
            or nb_device.get("firmware") != mrk_device.get("firmware")
            or nb_device.get("floor_id") != mrk_device.get("floor_id")
            or nb_device.get("lan_ip") != mrk_device.get("lan_ip")
            or nb_device.get("tags") != mrk_device.get("tags")
            or nb_device.get("wan_primary_ip") != mrk_device.get("wan_primary_ip")
            or nb_device.get("wan_secondary_ip") != mrk_device.get("wan_secondary_ip")
        ):
            update_fields = {
                "id": nb_device["id"],
                "site": site_nb["id"],
                "custom_fields": {
                    "asset_url": mrk_device.get("asset_url"),
                    "firmware": mrk_device.get("firmware"),
                    "floor_id": mrk_device.get("floor_id"),
                    "lan_ip": mrk_device.get("lan_ip"),
                    "tags": mrk_device.get("tags"),
                    "wan_primary_ip": mrk_device.get("wan_primary_ip"),
                    "wan_secondary_ip": mrk_device.get("wan_secondary_ip"),
                },
            }
            devices_to_update.append(update_fields)

    devices_to_delete = [
        device["id"]
        for name, device in devices_nb_by_name.items()
        if name not in names_mrk
    ]

    devices_to_create = [
        {
            "name": device["name"],
            "role": device["device_role"],
            "device_type": device["device_type"],
            "serial_number": device["serial_number"],
            "asset_tag": asset_tag,
            "status": "active",
            "site": site_nb["id"],
            "custom_fields": {
                "asset_url": device["asset_url"],
                "firmware": device["firmware"],
                "floor_id": device["floor_id"],
                "lan_ip": device["lan_ip"],
                "tags": device["tags"],
                "wan_primary_ip": device["wan_primary_ip"],
                "wan_secondary_ip": device["wan_secondary_ip"],
                "wireless_mac": device["wireless_mac"],
            },
        }
        for asset_tag, device in devices_mrk_by_asset_tag.items()
        if asset_tag not in asset_tags_nb
    ]

    if devices_to_delete:
        print("Devices to delete:", devices_to_delete)
        nb.dcim.devices.delete(devices_to_delete)

    if devices_to_create:
        print("Devices to create:", devices_to_create)
        nb.dcim.devices.create(devices_to_create)

    if devices_to_update:
        print("Devices to update:", devices_to_update)
        nb.dcim.devices.update(devices_to_update)
