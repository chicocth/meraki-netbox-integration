import os
import utils
import netboxHelper

# I use the environment that I have setup before in utils.py.
meraki_api_key, netbox_api_key, netbox_url = utils.setup_environment()
nb = utils.setup_netbox_client(netbox_url, netbox_api_key)
dashboard = utils.setup_meraki_client()


# Fetch organizations from Meraki and site groups from Netbox
orgs_mrk = dashboard.organizations.getOrganizations()
site_groups_nb_dict = nb.dcim.site_groups.all()

# Extract relevant data from Meraki and Netbox responses
orgs_mrk_dict = [{"org_key": org["id"], "name": org["name"]} for org in orgs_mrk]

orgs = netboxHelper.get_site_groups_info(nb)


site_groups_to_update = [
    {
        "id": group["id"],
        "name": org["name"],
        "slug": "-".join(org["name"].lower().split()),
        "description": org["org_key"],
    }
    for group in site_groups_nb_dict
    for org in orgs_mrk_dict
    if group["org_key"] == org["org_key"] and group["name"] != org["name"]
]

site_groups_to_delete = [
    group["id"]
    for group in site_groups_nb_dict
    if group["org_key"] not in {org["org_key"] for org in orgs_mrk_dict}
]
site_groups_to_create = [
    {
        "name": org["name"],
        "slug": "-".join(org["name"].lower().split()),
        "description": org["org_key"],
    }
    for org in orgs_mrk_dict
    if org["org_key"] not in {group["org_key"] for group in site_groups_nb_dict}
]


if site_groups_to_update:
    for site_group in site_groups_to_update:
        nb.dcim.site_groups.update([site_group])

if site_groups_to_delete:
    for site_group in site_groups_to_delete:
        nb.dcim.site_groups.delete([site_group])

if site_groups_to_create:
    for site_group in site_groups_to_create:
        nb.dcim.site_groups.create([site_group])
