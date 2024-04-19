# Introduction 
This repository contains scripts designed to facilitate the migration and integration of Meraki Devices into an organizational structure. While the scripts are still in an early stage and not yet production-ready for community consumption, they serve as a foundation for further development and improvement.

A device_matching.log file is provided to aid in identifying devices that do not exist in Netbox. All devices have been imported using the device_type library. However, there is still work to be done in populating additional device data, such as interface information per device in Netbox.

The requirements.txt file lists necessary dependencies for running the scripts. Additionally, custom fields have been created in Netbox to accommodate specific use cases, and their export will be included in the repository.

To run the scripts, ensure you have a .env file in the root folder containing the following variables:

MERAKI_DASHBOARD_API_KEY=
NETBOX_API_KEY=
NETBOX_URL=
Feel free to clone this repository and contribute to its improvement!