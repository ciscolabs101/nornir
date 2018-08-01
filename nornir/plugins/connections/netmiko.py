from typing import Any, Dict, Optional, Union

from netmiko import ConnectHandler

from nornir.core.configuration import Config
from nornir.core.connections import ConnectionPlugin

napalm_to_netmiko_map = {
    "ios": "cisco_ios",
    "nxos": "cisco_nxos",
    "eos": "arista_eos",
    "junos": "juniper_junos",
    "iosxr": "cisco_xr",
}


class Netmiko(ConnectionPlugin):
    """
    This plugin connects to the device using the NAPALM driver and sets the
    relevant connection.

    Inventory:
        netmiko_options: maps to argument passed to ``ConnectHandler``.
        nornir_network_ssh_port: maps to ``port``
    """

    def open(
        self,
        hostname: str,
        username: str,
        password: str,
        ssh_port: int,
        network_api_port: int,
        operating_system: str,
        nos: str,
        connection_options: Optional[Dict[str, Any]] = None,
        configuration: Optional[Config] = None,
    ) -> None:

        parameters: Dict[str, Union[str, int]] = {
            "host": hostname,
            "username": username,
            "password": password,
        }
        if ssh_port:
            parameters["port"] = ssh_port

        if nos is not None:
            # Look device_type up in corresponding map, if no entry return the host.nos unmodified
            device_type = napalm_to_netmiko_map.get(nos, nos)
            parameters["device_type"] = device_type

        if connection_options is None:
            connection_options = {}

        netmiko_connection_args = parameters
        netmiko_connection_args.update(connection_options)
        self.connection = ConnectHandler(**netmiko_connection_args)

    def close(self) -> None:
        self.connection.disconnect()
