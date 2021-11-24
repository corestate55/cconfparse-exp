"""
Generate interface prop table for a network device config
"""

from __future__ import annotations
from typing import Sequence
from ciscoconfparse import CiscoConfParse
import pandas as pd
from interface_prop_table_record_base import InterfacePropTableRecordBase
from interface_prop_table_record_for_ios import InterfacePropTableRecordForIOS
from interface_prop_table_record_for_junos import InterfacePropTableRecordForJunos


class InterfacePropTable:
    """
    Interface properties for a device (config file)
    """

    def __init__(self, config: str, syntax: str = "ios") -> None:
        self.parser = CiscoConfParse(config=config, syntax=syntax)
        self.syntax = syntax
        self.records = self._new_records()

    def hostname(self) -> str:
        """Hostname of the device (config file)"""
        # `hostname hoge` for ios, `host-name hoge;` for junos
        hostname_re = r"host-?name\s+([^\s;]+)"
        hostname_conf = self.parser.find_objects(hostname_re)[0]
        return hostname_conf.re_match_typed(hostname_re)

    def _new_records_for_junos(self) -> Sequence[InterfacePropTableRecordForJunos]:
        units = []
        for intf in self.parser.find_objects(r"interface")[0].children:
            units.append(InterfacePropTableRecordForJunos(self.parser, intf))
            for unit in intf.re_search_children(r"unit\s+\d+"):
                units.append(InterfacePropTableRecordForJunos(self.parser, intf, unit))
        return units

    def _new_records_for_ios(self) -> Sequence[InterfacePropTableRecordForIOS]:
        return list(
            map(lambda c: InterfacePropTableRecordForIOS(self.parser, c), self.parser.find_objects(r"interface"))
        )

    def _new_records(self) -> Sequence[InterfacePropTableRecordBase]:
        if self.syntax == "junos":
            return self._new_records_for_junos()
        # default (syntax == ios)
        return self._new_records_for_ios()

    def generate_dataframe(self) -> pd.DataFrame:
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
