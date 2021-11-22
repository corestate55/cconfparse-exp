"""
Frontend of interface-props-table
"""

import argparse
import sys
import pandas as pd
from interface_prop_table import InterfacePropTable


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Make interface prop table with CiscoconfParse")
    parser.add_argument("--file", "-f", type=str, help="Config file (parse single file)")
    parser.add_argument("--csv", action="store_true", help="Output data as CSV to STDOUT")
    args = parser.parse_args()

    # print-omit avoidance
    pd.set_option("display.width", 300)
    pd.set_option("display.max_columns", 20)
    pd.set_option("display.max_rows", 200)

    if args.file:
        print("# parse config = %s" % args.file, file=sys.stderr)
        intf_prop_table = InterfacePropTable(args.file)
        print("# Found config file of %s" % intf_prop_table.hostname(), file=sys.stderr)
        df = intf_prop_table.generate_dataframe()
        if args.csv:
            print(df.to_csv(sys.stdout))
        else:
            print("# Table: ", file=sys.stderr)
            print(df)
    else:
        print("Config file not specified", file=sys.stderr)
        sys.exit(1)
