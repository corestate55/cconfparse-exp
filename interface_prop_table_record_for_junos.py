"""
A record of interface property table (props of a interface)
for Junos (-like configs)
"""

import re
from ciscoconfparse.ccp_util import IPv4Obj
from interface_prop_table_record_base import InterfacePropTableRecordBase


class InterfacePropTableRecordForJunos(InterfacePropTableRecordBase):
    """
    Properties of a interface-units
    """

    def __init__(self, parser, intf_conf, unit_conf=None):
        super().__init__(parser, intf_conf)
        self._unit = unit_conf  # if None, it means 'physical' interface (NOT unit)
        catalogue_to_merge = {
            "hostname_typed": re.compile(r"host-?name\s+(\S+)"),
            "interface_typed": re.compile(r"(\S+)"),
            "aggregated_ether_name": re.compile(r"^ae\d+"),
            "unit_typed": re.compile(r"unit\s+(\d+)"),
            "vlan_tagging": re.compile(r"(?:flexible-)?vlan-tagging"),
            "vlan_id_typed": re.compile(r"vlan-id\s+(\d+)"),
            "gigether_options": re.compile(r"gigether-options"),
            "802.3ad_typed": re.compile(r"802.3ad\s+(\S+)"),
            "802.3ad_func": lambda g: re.compile(r"802.3ad %s" % g),
            # prevent match bosh `family inet` and `family inet6`
            "family_inet": re.compile(r"family\s+inet$"),
            "ipv4_typed": re.compile(r"address\s+(\S+)"),
            "routing_instances": re.compile(r"routing-instances"),
            "routing_intf_func": lambda n: re.compile(r"interface %s" % n),
        }
        # regexp catalogue
        self._re = dict(self._re, **catalogue_to_merge)

    def _hostname(self):
        hostname_conf = self._parser.find_objects(self._re["hostname_typed"])[0]
        return hostname_conf.re_match_typed(self._re["hostname_typed"])

    @property
    def _is_unit(self):
        return not self._is_physical

    @property
    def _is_physical(self):
        return self._unit is None

    @property
    def _is_aggregated_ethernet(self):
        return re.match(self._re["aggregated_ether_name"], self._intf_unit_str())

    def _intf_unit_str(self):
        intf_str = self._intf.re_match_typed(self._re["interface_typed"])
        if self._is_unit:
            intf_str = "%s.%s" % (intf_str, self._unit.re_match_typed(self._re["unit_typed"]))
        return intf_str

    @property
    def interface(self):
        return self._host_interface_str(self._intf_unit_str())

    @property
    def switchport_mode(self):
        if self._is_unit:
            return "NONE"
        if self.allowed_vlans:
            return "TRUNK"
        return "NONE"

    @property
    def access_vlan(self):
        # TODO: vlan config
        return None

    @property
    def allowed_vlans(self):
        if self._is_unit:
            return None
        vlan_tagging_conf_list = self._intf.re_search_children(self._re["vlan_tagging"])
        if not vlan_tagging_conf_list:
            return None
        vid_conf_list = self._intf.re_search_children(self._re["vlan_id_typed"], recurse=True)
        if not vid_conf_list:
            return None
        return ",".join(list(map(lambda vc: vc.re_match_typed(self._re["vlan_id_typed"]), vid_conf_list)))

    @property
    def channel_group(self):
        if self._is_unit or self._is_aggregated_ethernet:
            return None
        ge_opts_conf_list = self._intf.re_search_children(self._re["gigether_options"])
        if not ge_opts_conf_list:
            return None
        lag_conf_list = ge_opts_conf_list[0].re_search_children(self._re["802.3ad_typed"])
        if not lag_conf_list:
            return None
        return lag_conf_list[0].re_match_typed(self._re["802.3ad_typed"])

    @property
    def channel_group_members(self):
        if self._is_unit:
            return []
        if self._is_aggregated_ethernet:
            return list(
                map(
                    lambda c: c.parent.parent.re_match_typed(self._re["interface_typed"]),
                    self._parser.find_objects(self._re["802.3ad_func"](self._intf_unit_str())),
                )
            )
        return []

    @property
    def primary_address(self):
        if self._is_physical:
            return None
        inet_conf_list = self._unit.re_search_children(self._re["family_inet"])
        if not inet_conf_list:
            return None
        address_lines = inet_conf_list[0].re_search_children(self._re["ipv4_typed"])
        if not address_lines:
            return None
        ipv4_obj = address_lines[0].re_match_typed(self._re["ipv4_typed"], result_type=IPv4Obj)
        return ipv4_obj.as_cidr_addr

    def _find_attached_vr(self):
        vr_conf_list = self._parser.find_objects(self._re["routing_instances"])
        if not vr_conf_list:
            return "default"
        for vr_conf in vr_conf_list[0].children:
            if vr_conf.re_search_children(self._re["routing_intf_func"](self._intf_unit_str())):
                return vr_conf.re_match_typed(self._re["interface_typed"])
        return "default"

    @property
    def vrf(self):
        # check ONLY layer3 interface
        if not self.primary_address:
            return "default"
        return self._find_attached_vr()
