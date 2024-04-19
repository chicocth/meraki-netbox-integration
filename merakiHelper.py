import logging
logging.basicConfig(
    filename="device_matching.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)

def get_devices_mrk_dict(site_facility, device_types_dict, dashboard):
    devices_mrk_dict = []
    devices_mrk = dashboard.networks.getNetworkDevices(networkId=site_facility)
    if devices_mrk:
        for device_mrk in devices_mrk:
            matching_device_types = [
                device_type
                for device_type in device_types_dict
                if device_mrk["model"] == device_type["part_number"]
            ]
            if matching_device_types:
                device_type = matching_device_types[0]
                devices_mrk_dict.append(
                    {
                        "name": device_mrk["name"],
                        "device_role": device_type["role"],
                        "device_type": device_type["id"],
                        "serial_number": device_mrk.get("serial", None),
                        "asset_tag": device_mrk.get("mac", None),
                        "status": "active",
                        "site": site_facility,
                        "asset_url": device_mrk["url"],
                        "firmware": device_mrk.get("firmware", None),
                        "floor_id": device_mrk.get("floorPlanId", None),
                        "lan_ip": device_mrk.get("lanIp", None),
                        "tags": " | ".join(device_mrk.get("tags", [])),
                        "wan_primary_ip": device_mrk.get("wan1Ip", None),
                        "wan_secondary_ip": device_mrk.get("wan2Ip", None),
                        "wireless_mac": device_mrk.get("wirelessMac", None),
                    }
                )
            else:
                logging.info(f"No matching device type found for part_number: {device_mrk['model']}")
    return devices_mrk_dict
