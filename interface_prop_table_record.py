"""
A record of interface property table (props of a interface)
"""

import re
from ciscoconfparse.ccp_util import IPv4Obj
from interface_prop_table_record_base import InterfacePropTableRecordBase


class InterfacePropTableRecord(InterfacePropTableRecordBase):
    """
    Properties of a interface
    """

    def __init__(self, parser, intf_conf):
        super().__init__(parser, intf_conf)
        catalogue_to_merge = {
            "interface_typed": re.compile(r"interface\s+(\S+)"),
            "access_vlan_typed": re.compile(r"switchport\s+access\s+vlan\s+(\d+)"),
            "allowed_vlan_typed": re.compile(r"switchport\s+trunk\s+allowed\s+vlan\s+(\S+)"),
            "switchport_mode_typed": re.compile(r"switchport\s+mode\s+(\w+)"),
            "channel_group_typed": re.compile(r"channel-group\s+(\d+)"),
            # `Port-channel`/`Port-Channel` pattern
            "channel_group_intf_func": lambda g: re.compile(r"^interface (Port-channel%s)" % g, re.IGNORECASE),
            # enable ignore-case: accept: both `Port-channel` and `Port-Channel`
            "channel_group_intf_typed": re.compile(r"^interface\s+Port-channel(\d+)", re.IGNORECASE),
            "channel_group_func": lambda g: re.compile(r"channel-group %s" % g),
            # `ipaddr netmask`/`ipaddr/prefix-len` pattern
            "ipv4_typed": re.compile(r"ip(?:v4)?\s+address\s+(.+)$"),
            "vrf_typed": re.compile(r"ip\s+vrf\s+forwarding\s+(\S+)"),
        }
        self._catalogue = dict(self._catalogue, **catalogue_to_merge)

    @property
    def interface(self):
        return self._host_interface_str(self._intf.re_match_typed(self._catalogue["interface_typed"]))

    @property
    def access_vlan(self):
        return self._intf.re_match_iter_typed(self._catalogue["access_vlan_typed"])

    @property
    def allowed_vlans(self):
        return self._intf.re_match_iter_typed(self._catalogue["allowed_vlan_typed"])

    @property
    def switchport_mode(self):
        """switchport mode (ACCESS/TRUNK/NONE)"""
        swp_mode = self._intf.re_match_iter_typed(self._catalogue["switchport_mode_typed"])
        if swp_mode:
            return swp_mode.upper()
        # in vEOS, access-port does not have `switchport mode` config line
        if self._intf.re_search_children(self._catalogue["access_vlan_typed"]):
            return "ACCESS"
        return "NONE"

    @property
    def channel_group(self):
        if self._intf.intf_in_portchannel:
            group_num_str = self._intf.re_match_iter_typed(self._catalogue["channel_group_typed"])
            return self._parser.re_match_iter_typed(self._catalogue["channel_group_intf_func"](group_num_str))
        return ""

    @property
    def channel_group_members(self):
        group_num_str = self._intf.re_match_typed(self._catalogue["channel_group_intf_typed"])
        # method `is_portchannel_intf` does not works...
        if not group_num_str:
            return []

        members = self._parser.find_objects_w_all_children(self._catalogue["interface_typed"],
                                                           [self._catalogue["channel_group_func"](group_num_str)])
        return list(map(lambda m: m.re_match_typed(self._catalogue["interface_typed"]), members))

    @property
    def primary_address(self):
        # accept  both`192.168.0.3 255.255.255.0` and `192.168.0.3/24`
        ipv4_conf_re = self._catalogue["ipv4_typed"]
        if self._intf.re_search_children(ipv4_conf_re):
            ipv4_obj = self._intf.re_match_iter_typed(ipv4_conf_re, result_type=IPv4Obj)
            return ipv4_obj.as_cidr_addr
        return ""

    @property
    def vrf(self):
        return self._intf.re_match_iter_typed(self._catalogue["vrf_typed"]) or "default"
