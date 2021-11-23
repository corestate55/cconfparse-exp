"""
Generate interface prop table for a network device config
"""

from ciscoconfparse import CiscoConfParse
import pandas as pd
from interface_prop_table_record import InterfacePropTableRecord


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
