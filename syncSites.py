import json
import utils
from decimal import Decimal
from helper.slugify import slugify
import netboxHelper

meraki_api_key, netbox_api_key, netbox_url = utils.setup_environment()
nb = utils.setup_netbox_client(netbox_url, netbox_api_key)
dashboard = utils.setup_meraki_client()

orgs = netboxHelper.get_site_groups_info(nb)


sites_mrk_dict = []

for org in orgs:
    networks = dashboard.organizations.getOrganizationNetworks(
        organizationId=org["org_key"]
    )
    for network in networks:
        my_devices = dashboard.networks.getNetworkDevices(networkId=network["id"])
        if (
            my_devices
        ):  # I still have to do a chain request for site_group -> description
            site_info = {
                "name": network["name"],
                "facility": network["id"],
                "site_group": org["id"],
                "organization_id": org["org_key"],
                "address": None,
                "latitude": None,
                "longitude": None,
                "devices": [],
            }
            for device in my_devices:
                if device["address"] and site_info["address"] is None:
                    site_info["address"] = device["address"]
                    site_info["latitude"] = float(
                        Decimal(device["lat"]).quantize(Decimal("0.000000"))
                    )
                    site_info["longitude"] = float(
                        Decimal(device["lng"]).quantize(Decimal("0.000000"))
                    )

                if device["name"] and device["serial"]:
                    device_data = {
                        "name": device["name"],
                        "serial": device["serial"],
                        "mac": device["mac"],
                        "wireless_mac": device.get("wirelessMac", None),
                        "model": device["model"],
                        "firmware": device["firmware"],
                        "lan_ip": device.get("lanIp", None),
                        "wan1_ip": device.get("wan1Ip", None),
                        "wan2_ip": device.get("wan2Ip", None),
                        "floor_id": device.get("floorPlanId", None),
                    }
                    site_info["devices"].append(device_data)

            sites_mrk_dict.append(site_info)

sites_nb_dict = netboxHelper.get_sites_nb_dict(nb)

sites_to_update = []

for site_nb in sites_nb_dict:
    for site_mrk in sites_mrk_dict:
        if site_nb["facility"] == site_mrk["facility"]:
            if site_nb["name"].strip().lower() != site_mrk["name"].strip().lower():
                updated_site = {
                    "id": site_nb["id"],
                    "name": site_mrk["name"],
                    "slug": slugify(site_mrk["name"]),
                    "status": "active",
                    "facility": site_mrk["facility"],
                    "physical_address": (
                        "" if site_mrk["address"] is None else site_mrk["address"]
                    ),
                    "shipping_address": (
                        "" if site_mrk["address"] is None else site_mrk["address"]
                    ),
                    "latitude": site_mrk["latitude"],
                    "longitude": site_mrk["longitude"],
                }
                sites_to_update.append(updated_site)


sites_to_delete = []

for site_nb in sites_nb_dict:
    if site_nb["facility"] not in {site_mrk["facility"] for site_mrk in sites_mrk_dict}:
        sites_to_delete.append(site_nb["id"])


sites_to_create = []

for site_mrk in sites_mrk_dict:
    if site_mrk["facility"] not in {site_nb["facility"] for site_nb in sites_nb_dict}:
        new_site = {
            "name": site_mrk["name"],
            "slug": slugify(site_mrk["name"]),
            "status": "active",
            "facility": site_mrk["facility"],
            "physical_address": (
                "" if site_mrk["address"] is None else site_mrk["address"]
            ),
            "shipping_address": (
                "" if site_mrk["address"] is None else site_mrk["address"]
            ),
            "latitude": site_mrk["latitude"],
            "longitude": site_mrk["longitude"],
        }
        sites_to_create.append(new_site)


if sites_to_delete:
    for site in sites_to_delete:
        nb.dcim.sites.delete([site])

if sites_to_update:
    for site in sites_to_update:
        nb.dcim.sites.update([site])


if sites_to_create:
    for site in sites_to_create:
        nb.dcim.sites.create([site])


# Map the site_groups to FK and able to match the stuff
# Insert timezone
# Check if we can do something about Tenant group
