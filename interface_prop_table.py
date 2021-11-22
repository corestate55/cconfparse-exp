"""
Generate interface prop table for a defice config
"""

import re
from ciscoconfparse import CiscoConfParse
from ciscoconfparse.ccp_util import IPv4Obj
import pandas as pd


class InterfacePropTableRecord:
    """
    Properties of a interface
    """

    def __init__(self, parser, intf_conf):
        self._parser = parser  # CiscoConfigParse
        self._intf_conf = intf_conf  # IOSCfgLine object of an interface

    def _hostname(self):
        return self._parser.re_match_iter_typed(r"^hostname\s+(.+)")

    @property
    def interface(self):
        """`hostname[interface]` format string"""
        return "%s[%s]" % (self._hostname(), self._intf_conf.re_match_typed(r".+\s+(.+)"))

    @property
    def switchport(self):
        """True if switchport"""
        return self.switchport_mode != "NONE"

    @property
    def switchport_mode(self):
        """switchport mode (ACCESS/TRUNK/NONE)"""
        mode = self._intf_conf.re_match_iter_typed(r"switchport\s+mode\s+(\w+)")
        if mode == "access":
            return "ACCESS"
        if mode == "trunk":
            return "TRUNK"
        return "NONE"

    @property
    def access_vlan(self):
        """Access vlan-id"""
        return self._intf_conf.re_match_iter_typed(r"switchport\s+access\s+vlan\s+(\d+)")

    @property
    def allowed_vlans(self):
        """Trunk vlan-ids (e.g. "1,3,5-8" string)"""
        return self._intf_conf.re_match_iter_typed(r"switchport\s+trunk\s+allowed\s+vlan\s+(.+)")

    @property
    def channel_group(self):
        """`Parent channel interface name of the interface"""
        if self._intf_conf.intf_in_portchannel:
            group_num_str = self._intf_conf.re_match_iter_typed(r"channel-group\s+(\d+)")
            # there is `Port-channel`/`Port-Channel` pattern
            group_intf_re = re.compile(r"^interface (Port-channel%s)" % group_num_str, re.IGNORECASE)
            return self._parser.re_match_iter_typed(group_intf_re)
        return ""

    @property
    def channel_group_members(self):
        """Children interface name of the channel interface"""
        # enable ignore-case: accept: both `Port-channel` and `Port-Channel`
        group_re = re.compile(r"^interface\s+Port-channel(\d+)", re.IGNORECASE)
        # method `is_portchannel_intf` does not works...
        group_num_str = self._intf_conf.re_match_typed(group_re)
        if group_num_str:
            return list(
                map(
                    lambda conf: conf.parent.re_match_typed(r"interface\s+(.+)"),
                    self._parser.re_search_children(r"channel-group %s" % group_num_str, recurse=True),
                )
            )
        return []

    @property
    def primary_address(self):
        """IPv4 address of the interface"""
        # accept  both`192.168.0.3 255.255.255.0` and `192.168.0.3/24`
        ipv4_conf_re = re.compile(r"ip(?:v4)?\s+address\s+(.+)$")
        if self._intf_conf.re_search_children(ipv4_conf_re):
            ipv4_obj = self._intf_conf.re_match_iter_typed(ipv4_conf_re, result_type=IPv4Obj)
            return ipv4_obj.as_cidr_addr
        return ""

    @property
    def vrf(self):
        """VRF name of the interface"""
        return self._intf_conf.re_match_iter_typed(r"ip\s+vrf\s+forwarding\s+(.+)") or "default"


class InterfacePropTable:
    """
    Interface properties for a device (config file)
    """

    def __init__(self, config):
        self.parser = CiscoConfParse(config=config)
        self.records = self._records()

    def hostname(self):
        """Hostname of the device (config file)"""
        return self.parser.re_match_iter_typed(r"^hostname\s+(.+)")

    def _records(self):
        return list(
            map(
                lambda c: InterfacePropTableRecord(self.parser, c),
                self.parser.find_objects(r"^interface"),
            )
        )

    def generate_dataframe(self):
        """Generate interface properties table as a Dataframe"""
        cols = [
            "Interface",
            "Access_VLAN",
            "Allowed_VLANs",
            "Channel_Group",
            "Channel_Group_Members",
            "Primary_Address",
            "Switchport",
            "Switchport_mode",
            "VRF",
        ]
        data = list(
            map(
                lambda rec: list(map(lambda col: getattr(rec, col.lower()), cols)),
                self.records,
            )
        )
        return pd.DataFrame(data, columns=cols)
