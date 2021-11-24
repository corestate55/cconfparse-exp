"""
Abstract class of interface-property-table record
"""

from __future__ import annotations
from abc import ABC, abstractmethod
import re
from ciscoconfparse import CiscoConfParse, IOSCfgLine


class InterfacePropTableRecordBase(ABC):
    """
    Abstract class of interface-property-table record
    """

    def __init__(self, parser: CiscoConfParse, intf_conf: IOSCfgLine) -> None:
        self._parser = parser  # CiscoConfParse
        self._intf = intf_conf  # IOSCfgLine object of an interface
        # regexp catalogue
        self._re: dict = {
            "hostname_typed": re.compile(r"hostname\s+(.+)"),
        }

    def _hostname(self) -> str:
        return self._parser.re_match_iter_typed(self._re["hostname_typed"])

    def _host_interface_str(self, interface_str: str) -> str:
        return "%s[%s]" % (self._hostname(), interface_str)

    @property
    @abstractmethod
    def interface(self) -> None | str:
        """`hostname[interface]` format string"""
        return None

    @property
    def switchport(self) -> bool:
        """True if switchport"""
        return self.switchport_mode != "NONE"

    @property
    @abstractmethod
    def switchport_mode(self) -> None | str:
        """switchport mode (ACCESS/TRUNK/NONE)"""
        return "NONE"

    @property
    @abstractmethod
    def access_vlan(self) -> None | str:
        """Access vlan-id"""
        return None

    @property
    @abstractmethod
    def allowed_vlans(self) -> None | str:
        """Trunk vlan-ids (e.g. "1,3,5-8" string)"""
        return None

    @property
    @abstractmethod
    def channel_group(self) -> None | str:
        """`Parent channel interface name of the interface"""
        return None

    @property
    @abstractmethod
    def channel_group_members(self) -> list:
        """Children interface name of the channel interface"""
        return []

    @property
    @abstractmethod
    def primary_address(self) -> None | str:
        """IPv4 address of the interface"""
        return None

    @property
    @abstractmethod
    def vrf(self) -> None | str:
        """VRF name of the interface"""
        return None
