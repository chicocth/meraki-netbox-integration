import os
from dotenv import load_dotenv
import requests
from urllib3.exceptions import InsecureRequestWarning
import meraki
import pynetbox

def setup_environment():
    # Loads .env file and its variables
    load_dotenv()
    meraki_api_key = os.getenv("MERAKI_DASHBOARD_API_KEY")
    netbox_api_key = os.getenv("NETBOX_API_KEY")
    netbox_url = os.getenv("NETBOX_URL")

    # Disable the warning for insecure HTTPS requests
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    return meraki_api_key, netbox_api_key, netbox_url

def setup_netbox_client(netbox_url, netbox_api_key):
    return pynetbox.api(netbox_url, token=netbox_api_key)

def setup_meraki_client():
    return meraki.DashboardAPI(suppress_logging=True)
