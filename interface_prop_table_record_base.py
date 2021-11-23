"""
Abstract class of interface-property-table record
"""

from abc import ABC, abstractmethod
import re


class InterfacePropTableRecordBase(ABC):
    """
    Abstract class of interface-property-table record
    """

    def __init__(self, parser, intf_conf):
        self._parser = parser  # CiscoConfigParse
        self._intf = intf_conf  # IOSCfgLine object of an interface
        self._catalogue = {
            "hostname_typed": re.compile(r"hostname\s+(.+)"),
        }

    def _hostname(self):
        return self._parser.re_match_iter_typed(self._catalogue["hostname_typed"])

    def _host_interface_str(self, interface_str):
        return "%s[%s]" % (self._hostname(), interface_str)

    @property
    @abstractmethod
    def interface(self):
        """`hostname[interface]` format string"""
        return ""

    @property
    def switchport(self):
        """True if switchport"""
        return self.switchport_mode != "NONE"

    @property
    @abstractmethod
    def switchport_mode(self):
        """switchport mode (ACCESS/TRUNK/NONE)"""
        return "NONE"

    @property
    @abstractmethod
    def access_vlan(self):
        """Access vlan-id"""
        return ""

    @property
    @abstractmethod
    def allowed_vlans(self):
        """Trunk vlan-ids (e.g. "1,3,5-8" string)"""
        return ""

    @property
    @abstractmethod
    def channel_group(self):
        """`Parent channel interface name of the interface"""
        return ""

    @property
    @abstractmethod
    def channel_group_members(self):
        """Children interface name of the channel interface"""
        return []

    @property
    @abstractmethod
    def primary_address(self):
        """IPv4 address of the interface"""
        return ""

    @property
    @abstractmethod
    def vrf(self):
        """VRF name of the interface"""
        return ""
