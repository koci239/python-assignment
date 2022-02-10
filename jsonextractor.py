import json
from json.decoder import JSONDecodeError
from typing import Dict, List


class JSONExtractor():
    """Class to get information about interfaces from config file."""

    def __init__(self, config_file: str) -> None:
        """Initialization of JSONExtractor object.

        Args:
            config_file (str): Path to config file in JSON format.
        """
        self.config_file = config_file
        self.data = self._load_config()

    def _load_config(self) -> Dict:
        """Helper to open config file and parse it to JSON object.

        Returns:
            dict: Config file as JSON object.
        """
        with open(self.config_file, 'r') as config:
            return json.load(config)

    def get_interfaces(self, types: List[str]) -> List:
        """Method to get information about interfaces.

        Args:
            types (list[str]): List with name of interfaces to fetch information about.

        Returns:
            list[list[str]]: List with information about interfaces. Each in separated list.
        """
        list_of_interfaces = []
        topology = self.data.get("frinx-uniconfig-topology:configuration", {})
        interface_groups = topology.get(
            "Cisco-IOS-XE-native:native",
            {}).get(
            "interface",
            {})

        for type in types:
            for interface_info in interface_groups.get(type, {}):

                # interface group name + interface name
                name = f"{type}{interface_info['name']}"
                # interface description
                description = interface_info.get("description", None)
                # mtu from interface configuration
                max_frame_size = interface_info.get("mtu", None)
                # whole interface configuration
                config = interface_info
                # port-channel name, which is linked to Ethernet interfaces
                port_number = interface_info.get(
                    "Cisco-IOS-XE-ethernet:channel-group", {}) \
                    .get("number", None)
                port_channel_name = f"{'Port-channel'}{port_number}" if port_number else None

                list_of_interfaces.append(
                    [name, description, max_frame_size, config, port_channel_name])

        return list_of_interfaces
