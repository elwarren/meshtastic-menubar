import json
import os
import datetime as dt

from .menu import *
from .device import MeshtasticMenubar


def cli():
    """This is __main__ code when called as cli vs testing."""

    mm = MeshtasticMenubar()
    #
    # show menu bar icon asap so that if we throw exception we still have a menu
    #
    print_menu_icon(mm)

    mm.no_device = False
    mm.test_empty = False

    #
    # get meshtastic interface depending on connection type
    #
    # mm.iface = mm.get_iface()
    iface = mm.get_iface()

    if mm.iface is None:
        print("No connection method set")
        print("Choose wifi, ble, or serial")
        mm.no_device = "No connection method set"
        print_menu_debug(mm, mm, depth=0)
        print_menu_environment(mm, depth=1)
        print_menu_config(mm, depth=1)
        # should we exit 0 or 1? how does xbar handle this vs swiftbar?
        exit(0)

    nodes = mm.get_nodes()

    if mm.debug:
        print("Environment:\n", json.dumps(dict(os.environ)))
        print("Nodes:\n", json.dumps(mm.nodes))
        exit(0)

    #
    # main menu display output
    #
    print_menu_bar(mm, depth=0)

    #
    # menu drop down begin
    #
    print_menu_about(mm, depth=1)
    print_menu_refresh(mm, depth=1)
    print_menu_broadcast(mm, depth=1)
    print_menu_device(mm, depth=1)

    print_menu_debug(mm, depth=1)
    print_menu_environment(mm, depth=2)
    print_menu_config(mm, depth=2)
    print_menu_versions(mm, depth=2)

    print_menu_help(mm, depth=1)

    #
    # back to main menu again
    #
    print(f"Every: {mm.interval}m Last Run:")
    print(f"{mm.ts.replace(microsecond=0)}")
    print("---")

    # bail out if no nodes nothing to show
    if mm.test_empty or mm.no_device or len(mm.nodes) < 1:
        print(f"{mm.icon['police']} No Device or Nodes!")
        # show no_device holds our exception text
        print(mm.no_device)
        exit(0)

    print_menu_nodes(mm.nodes)
    #
    # End nodes submenu
    #

    #
    # Final act
    #
    mm.save_wifi_report()
    mm.save_nodes_csv()
    mm.save_nodes_jsonl()

    mm.iface.close
    # currently 13 seconds with uv on m2, not bad when running every 5m, mostly waiting on radio
    print(f"Runtime: {dt.datetime.now() - mm.ts}")
