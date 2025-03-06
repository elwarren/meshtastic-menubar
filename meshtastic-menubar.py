#!/opt/homebrew/bin/uv run --no-project --with pytap2 --with meshtastic[cli] --python 3.12 --script
# -*- coding: utf-8 -*-
#
# Show meshtastic nodes and stats in the menubar
#
# <xbar.title>Meshtastic Menubar</xbar.title>
# <xbar.version>v0.9</xbar.version>
# <xbar.author>elwarren</xbar.author>
# <xbar.author.github>elwarren</xbar.author.github>
# <xbar.desc>Show meshtastic nodes and stats in the menubar.</xbar.desc>
# <xbar.dependencies>python,uv,meshtastic</xbar.dependencies>
# <xbar.abouturl>https://github.com/elwarren/meshtastic-menubar</xbar.abouturl>
#
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pytap2",
#     "pyyaml",
#     "requests",
#     "meshtastic[cli]",
# ]
# ///


import datetime as dt

ts = dt.datetime.now()
import os
import json
import meshtastic
from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

VERSION = "v0.9"


def load_config() -> dict:
    """Returns dict with config paramaters. Sets defaults, then overrides with params from file."""

    config = {
        "connection": "wifi",
        "wifi_host": "meshtastic.local",
        "use_https": False,
        "debug": False,
        "log_nodes_jsonl": "meshtastic-menubar-nodes.jsonl",
        "log_nodes_csv": "meshtastic-menubar-nodes.csv",
        "log_wifi_report": "meshtastic-menubar-wifi-report.json",
        "log_traceroute_log": "meshtastic-menubar-traceroute.log",
        "log_dir": get_xdg_path("data_dir"),
        "bitbar": "xbar",
        "font_mono": "Menlo-Regular",
        "interval": 5,
        "meshtastic_bin": "meshtastic",
        "meshtastic_p1": "--host",
        "meshtastic_p2": "meshtastic.local",
    }
    config_path = get_xdg_path(file_type="config_file")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            new_config = load(f.read(), Loader=Loader)
            config.update(new_config)
    config["file"] = config_path
    return config


def get_xdg_path(file_type: str) -> str:
    """Return file path for config file in $XDG_CONFIG_HOME if it exists else $HOME"""

    if file_type == "config_file":
        if os.environ.get("XDG_CONFIG_HOME"):
            return os.path.expanduser(
                f"{os.environ.get('XDG_CONFIG_HOME')}/meshtastic-menubar.yml"
            )
        else:
            return os.path.expanduser(
                f"{os.environ.get('HOME')}/.meshtastic-menubar.yml"
            )

    if file_type == "data_dir":
        if os.environ.get("XDG_DATA_DIR"):
            return os.path.expanduser(
                f"{os.environ.get('XDG_DATA_DIR')}/meshtastic-menubar"
            )
        else:
            return os.path.expanduser(os.environ.get("HOME"))


def recursive_copy(obj: dict | list) -> dict:
    """Copy each record to a new `dict` but skip any keys named `raw` because they cannot be sesrialized to JSON"""

    # print(type(obj), obj)
    if isinstance(obj, dict):
        return {k: recursive_copy(v) for k, v in obj.items() if k != "raw"}
    elif isinstance(obj, list):
        return [recursive_copy(i) for i in obj]
    else:
        return obj


def seconds_to_dhms(seconds: int) -> tuple[int, int, int, int]:
    """Compute days, hours, minutes, seconds from total seconds"""

    days = seconds // (24 * 3600)
    remaining_seconds = seconds % (24 * 3600)

    hours = remaining_seconds // 3600
    remaining_seconds = remaining_seconds % 3600

    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60

    return days, hours, minutes, seconds


def menu_line(line: str, depth: int = 0) -> str:
    """Build a bitbar menu line at variable depths"""
    return "--" * depth + line


def print_menu_debug(depth: int = 1):
    """Build and display Debug submenu"""

    print(menu_line(f"{icon['exclaim']} Debug", depth))


def print_menu_environment(depth: int = 1):
    """Build and display Debug Nodelist submenu"""

    print(menu_line("Environment", depth=depth))
    for var in sorted(os.environ):
        print(menu_line(f"{var}={os.environ[var]}", depth=depth + 1))

def print_menu_nodelist(nodelist: str, depth: int = 1):
    """Build and display Debug Nodelist submenu"""

    print(menu_line("Node List", depth=depth))
    for nodelist_node in nodelist:
        print(menu_line(f"Node: {nodelist_node}", depth=depth + 1))


def print_menu_config(config: str, depth: int = 1):
    """Build and display Configuration submenu"""

    print(menu_line(f"Config", depth=depth))
    print(
        menu_line(
            f"Edit Config File: {config['file']} | shell='vi' | terminal=true | param1={config['file']}",
            depth=depth + 1,
        )
    )

    for param in sorted(config):
        print(menu_line(f"{param}={config[param]}", depth=depth + 1))


git_repo_url = "https://github.com/elwarren/meshtastic-menubar"
git_zip_url = "https://github.com/meshtastic/python/archive/refs/heads/master.zip"
meshtastic_home_url = "https://meshtastic.org/"
meshtastic_repo_url = "https://github.com/meshtastic/python/"
xbar_repo_url = "https://github.com/matryer/xbar/"
swiftbar_repo_url = "https://github.com/swiftbar/SwiftBar/"
argos_repo_url = "https://github.com/p-e-w/argos"

# icons to choose from
icon = {
    "green": "🟢",
    "yellow": "🟡",
    "orange": "🟠",
    "red": "🔴",
    "blue": "🔵",
    "purple": "🟣",
    "brown": "🟤",
    "black": "⚫",
    "white": "⚪",
    "police": "🚨",
    "ticket": "🎫",
    "person": "👤",
    "people": "👥",
    "voltage": "⚡",
    "battery": "🔋",
    "battery_low": "🪫",
    "plug": "🔌",
    "pager": "📟",
    "satdish": "📡",
    "satellite": "🛰️",
    "telescope": "🔭",
    "bars": "📶",
    "hash": "#️⃣",
    "star": "*️⃣",
    "one": "1️⃣",
    "two": "2️⃣",
    "three": "3️⃣",
    "four": "4️⃣",
    "five": "5️⃣",
    "six": "6️⃣",
    "seven": "7️⃣",
    "eight": "8️⃣",
    "nine": "9️⃣",
    "globe_mesh": "🌐",
    "globe_america": "🌎",
    "compass": "🧭",
    "tent": "⛺",
    "office": "🏢",
    "house": "🏠",
    "gear": "⚙️",
    "settings": "⚙️",
    "trash": "🗑️",
    "about": "🆎",
    "question": "❓",
    "exclaim": "❗",
    "refresh": "🔄",
    "waffle": "🧇",
    "pancakes": "🥞",
    "wave": "👋",
    "thumbsup": "👍",
    "thumbsdown": "👎",
    "victory": "✌️",
    "horns": "🤘",
    "ok_hand": "👌",
    "ok_button": "🆗",
    "prohibited": "🚫",
    "one_hundred": "💯",
    "spider": "🕷️",
}

# TODO what are valid telemetry types?
telemetry_types = [
    "gps",
    "battery",
    "position",
    "user",
    "device",
]

# TODO move this to optional txt pack that can be loaded without changing code
txts = [
    "Greetings",
    "Hello world!",
    "Hooty hoo!",
    "Howdy",
    # TODO nested apostrophes break shell, need function to escape on send
    "What up?",
    "New phone who dis?",
    "Good morning!",
    "Good night!",
    "Later",
    "Enroute",
    "Arrived",
    "Negative",
    "Affirmative",
    "Yes",
    "No",
    "LOL",
    "ROFL",
    # "WTF",
    # "SOS",
    icon["wave"],
    icon["thumbsup"],
    icon["thumbsdown"],
    icon["victory"],
    icon["horns"],
    icon["ok_hand"],
    icon["prohibited"],
    icon["one_hundred"],
    "Eyes on",
    "Breakfast",
    "Brunch",
    "Lunch",
    "Supper",
    "Dinner",
    "Dessert",
    "Snacks",
    "Drinks",
    "Coffee",
    "Tea",
    "Beer",
    "Wine",
]

# base64 encoded image of Meshtastic logo
menu_icon = "iVBORw0KGgoAAAANSUhEUgAAADIAAAAcCAYAAAAjmez3AAAACXBIWXMAAA7DAAAOwwHHb6hkAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAApZJREFUWIXtmE2ITWEYx38zjvFthiFfC5OFaCZFJE2RRCIlysJuFGUxiVkYiylFmWxYTBGbWY2PUhJlwyyFSPmIhOQrYyjEmOHeY3Hcuce5/zPnOfe8d6H86yzuvc/vef7nve857/O+8F8AjAJ2AzUZctQB1W7slK92wAfuA4tTsjXAOSAP9AEr3Vqzqwn4QXAjPjAIHACqjHxniPWBD8BM9zZHlgfcjhjxgTNGfgXwS/CXnDtN0CFh4i1Qb2DHA08EX7haKuBXagkwJAxsNPJdgg1fn4G5bi2XagzwQBQ/beTXEDzcYTb62QeuU+E32TFR9AUw2cDWAi8Fv4PgrRf9fo9j78NqBnKRYjlgtZHvptTsxT+/qek6ADS6sV7UBOCpMHLcyG8SbB8wIxRzUMTcAUZndh/SKVHkMTDOwE4D3gl+ayTOA26JuI7s9gOtpfSB/AksN/LnhbnumNiFwHdRa1l51ouqA14JI4eN/HbBvgamjMC0CeYRMDa9/aJ6RNJ72JrE2cDHCJsH1idw1UCvqHs0vf1Am0WyQWCRkb8i+C4j2wB8ibA5YJWRH9Z04L0w0m7kdwn2GTAxhYedIsdzYFKKHFwQSW4Q7D+S1IAezXLa9MvCx0kr3CLgb8B8Axs3vzvt3v/SLKA/kisPbEgC5wCfhJFWY+F9gn1ItjfOFpHzDTA1DqgCrgroGrbN0gL0GrC03DsI6azw1RMX3CqCrS21B9wUvKtVOW492xYNnAd8FYHWTU6HYF33Seso7TD6iWyPTwgj1m1nPaWDMEDQbriW6vmOhAM8YD/Fw4S0BwGNBP9AIfnezJa1wl34EEHHLJeEJuAuYu4ZVBiM3rjkjtRM0CYlHj95GQtV8iYKsh45/Xv6DTfbUnnkjAuSAAAAAElFTkSuQmCC"


def cli(config: dict):
    """This is __main__ code when called as cli vs testing."""

    # show menu bar icon asap so that if we throw exception we still have a menu
    print(f" | templateImage='{menu_icon}'")
    print("---")

    # HACK to get the shell bar separators to work in xbar and swiftbar
    B = "|"
    SHELL = "shell"

    no_device = False
    test_empty = False

    # Maybe http saves some battery because https uses more cpu
    if config.get("use_https"):
        target_url = f"https://{config['wifi_host']}"
    else:
        target_url = f"http://{config['wifi_host']}"

    nodes = {}
    if config.get("connection") == "wifi":
        # TODO is importing late bad style? Trying to reduce imports and speed startup
        try:
            import meshtastic.tcp_interface

            iface = meshtastic.tcp_interface.TCPInterface(
                hostname=config.get("wifi_host")
            )
            nodes = recursive_copy(iface.nodes)
            iface.close()
            config["meshtastic_p1"] = "--host"
            config["meshtastic_p2"] = config["wifi_host"]
        except Exception as e:
            print(f"Exception connecting host: {config.get('wifi_host')} via Wifi: {e}")
            no_device = str(e)
            # TODO hostname does not resolve, usually because using serial or bluetooth
            # Exception connecting via Wifi: [Errno 8] nodename nor servname provided, or not known
            # [Errno 8] nodename nor servname provided, or not known

    elif config.get("connection") == "ble":
        try:
            import meshtastic.ble_interface

            iface = meshtastic.ble_interface.BLEInterface(
                address=config.get("ble_name")
            )
            nodes = recursive_copy(iface.nodes)
            iface.close()
            config["meshtastic_p1"] = "--ble"
            config["meshtastic_p2"] = config.get("ble_name")
        except Exception as e:
            print(f"Exception connecting via Bluetooth: {e}")
            no_device = str(e)

    elif config.get("connection") == "serial":
        try:
            import meshtastic.serial_interface

            iface = meshtastic.serial_interface.SerialInterface(
                config.get("serial_port")
            )
            nodes = recursive_copy(iface.nodes)
            iface.close()

            config["meshtastic_p1"] = "--port"
            config["meshtastic_p2"] = config.get("serial_port")
        except Exception as e:
            print(f"Exception connecting via Serial: {e}")
            no_device = str(e)
            # TODO Exception connecting via Serial: [Errno 35] Could not exclusively lock port /dev/cu.usbserial-0001: [Errno 35] Resource temporarily unavailable
    else:
        print("No connection method set")
        print("Choose wifi, ble, or serial")
        no_device = "No connection method set"
        print_menu_debug(depth=0)
        print_menu_environment(depth=1)
        print_menu_config(config, depth=1)
        # should we exit 0 or 1? how does xbar handle this vs swiftbar?
        exit(0)

    # log nodes early incase we are debugging and skip gui
    if config.get("log_nodes_jsonl"):
        with open(
            f"{config.get('log_dir')}/{config.get('log_nodes_jsonl')}",
            "a",
            encoding="utf-8",
        ) as f:
            # HACK skipkeys is fix for Position not serializable only on serial not wifi
            f.write(
                # json.dumps({"timestamp": str(ts), "nodes": nodes}, skipkeys=True) + "\n"
                json.dumps({"timestamp": str(ts), "nodes": nodes})
                + "\n"
            )

    if config.get("debug"):
        print("Environment:\n", json.dumps(dict(os.environ)))
        print("Nodes:\n", json.dumps(nodes))
        exit(0)

    nodelist = []
    if no_device:
        pass
    else:
        # NOTE default lastHeard to zero because relayed nodes do not report and we need this to sort
        nodelist = sorted(
            nodes, reverse=True, key=lambda x: nodes[x].get("lastHeard", 0)
        )

    #
    # main menu display output
    #
    # menu drop down begin
    #
    print(f"Meshtastic Menubar")

    print("-----")
    print(f"--{icon['waffle']} About")
    print(f"----Meshtastic Menubar | href={git_repo_url}")
    print(f"----Version: {VERSION} | href={git_zip_url}")

    print("-------")
    print("----Built with:")
    print(f"----Meshtastic Project | href={meshtastic_home_url}")
    print(f"----Meshtastic Python | href={meshtastic_repo_url}")
    print(f"----xbar (bitbar) | href={xbar_repo_url}")
    print(f"----Swiftbar | href={swiftbar_repo_url}")
    print(f"----Argos | href={argos_repo_url}")

    print("-----")
    print(f"--{icon['refresh']} Refresh | refresh=true")

    print(f"--{icon['satellite']} Broadcast")

    for txt in txts:
        # TODO new machine has different setup than my build machine. zsh: command not found: meshtastic
        # TODO i hate shell escaping in these apps
        # "meshtastic.local" 'meshtastic' --port /dev/cu.usbserial-0001 --sendtext What up?
        # zsh: no matches found: up?
        print(
            f"----{txt} | {SHELL}='meshtastic' {B} terminal=true {B} param1={config['meshtastic_p1']} {B} param2={config['meshtastic_p2']} {B} param3='--sendtext' {B} param4='{txt}'"
        )

    print(f"--{icon['gear']} Device")
    print(
        f"----Reboot | {SHELL}='meshtastic' {B} terminal=true {B} param1={config['meshtastic_p1']} {B} param2={config['meshtastic_p2']} {B}param3='--reboot'"
    )
    print(
        f"----Shutdown | {SHELL}='meshtastic' {B} terminal=true {B} param1={config['meshtastic_p1']} {B} param2={config['meshtastic_p2']} {B}param3='--shutdown'"
    )
    print(
        f"----Tail logs | {SHELL}='meshtastic' {B} terminal=true {B} param1={config['meshtastic_p1']} {B} param2={config['meshtastic_p2']} {B}param3='--noproto'"
    )
    print(
        f"----BLE Scan | {SHELL}='meshtastic' {B} terminal=true {B} param1={config['meshtastic_p1']} {B} param2={config['meshtastic_p2']} {B}param3='--ble-scan'"
    )
    print(
        f"----json Report | {SHELL}='open' {B} terminal=false {B} param1='{target_url}/json/report'"
    )

    print_menu_debug(depth=1)
    print_menu_environment(depth=2)
    print_menu_config(config, depth=2)
    print_menu_nodelist(nodelist, depth=2)

    print("-----")
    print(f"--{icon['question']} Help")
    print("----🟢 Green nodes have been heard in past hour")
    print("----🟡 Yellow nodes three hours")
    print("----🟠 Orange 12 hours")
    print("----🔴 Red past three days")
    print("----🟣 Purple heard in past seven days")
    print("----🔵 Blue nodes are ice cold, we haven't heard from them in over a week")
    print("----⚫ Black nodes were partially received without timestamp")
    print("-------")
    print(f"----📚 RTFM | href='{git_repo_url}'")

    #
    # back to main menu again
    #
    print(f"Every: {config['interval']}m Last Run:")
    print(f"{ts.replace(microsecond=0)}")
    print("---")

    # bail out if no nodes nothing to show
    if test_empty or no_device or len(nodelist) < 0:
        print(f"{icon['police']} No Device or Nodes!")
        # show no_device holds our exception text
        print(no_device)
        exit(0)

    print("---")
    print(f"Nodes: {len(nodelist)}")

    first_node = True
    for node in nodelist:
        n = nodes[node]

        # have to reach into potentially missing keys to build main menu
        try:
            _name_short = n["user"].get("shortName")
        except:
            _name_short = None

        heard_last = n.get("lastHeard")

        # if heard_last is None then black because we can't calculate time without it
        status_icon = icon["black"]
        heard_str = "Not Reported"
        heard_ago = None
        heard_ago_total_seconds = None
        heard_at_dt = None

        if heard_last:
            heard_at_dt = dt.datetime.fromtimestamp(heard_last)
            # calculate time in seconds since last heard
            heard_ago = ts - heard_at_dt
            heard_ago_total_seconds = int(heard_ago.total_seconds())
            heard_days, heard_hours, heard_minutes, heard_seconds = seconds_to_dhms(
                heard_ago_total_seconds
            )

            if config["debug"]:
                print(
                    f"heard_ago {heard_ago} = now {ts} - heard_at_dt {heard_at_dt} heard_ago_seconds {heard_ago_total_seconds}"
                )

            # blue is on ice because it's been over a week since we heard from them
            status_icon = icon["blue"]

            # purple if heard in last week
            if heard_days < 8:
                status_icon = icon["purple"]

            # red if heard in last 3 days
            if heard_days < 4:
                status_icon = icon["red"]

            # orange if heard in last 12 hours 43200 sec
            if heard_ago_total_seconds < (12 * 60 * 60):
                status_icon = icon["orange"]

            # yellow if heard in last three hours 10800 sec
            if heard_ago_total_seconds < (3 * 60 * 60):
                status_icon = icon["yellow"]

            # green if heard in last hour 3600 sec
            if heard_ago_total_seconds < (1 * 60 * 60):
                status_icon = icon["green"]

            heard_str = (
                f"{heard_days}d {heard_hours}h {heard_minutes}m {heard_seconds}s"
            )

        #
        # First line is always our node so it gets a special mesh icon
        #
        if first_node:
            first_node = False
            print(
                f"{icon['globe_mesh']} {node} - {_name_short} | font={config['font_mono']}"
            )
        else:
            print(f"{status_icon} {node} - {_name_short} | font={config['font_mono']}")

        #
        # First submenu
        #
        # Heard submenu
        #
        print(f"--{icon['satdish']} Heard")
        print(f"--SNR: {n.get('snr')} | href='{target_url}'")
        print(f"--Hops away: {n.get('hopsAway')} | href='{target_url}'")
        print(f"--Last: {heard_str}| href='{target_url}'")
        print(f"--Seconds: {heard_ago_total_seconds}| href='{target_url}'")
        print(f"--DT: {heard_at_dt}| href='{target_url}'")
        # print(f"--Epoc: {heard_last}| href='{target_url}'")

        #
        # User submenu
        #
        if n.get("user"):
            print("-----")
            print(f"--{icon['ticket']} User")
            print(f"--Name: {n['user'].get('longName')} | href='{target_url}'")
            print(f"--Short: {n['user'].get('shortName')} | href='{target_url}'")
            print(f"--Model: {n['user'].get('hwModel')} | href='{target_url}'")
            print(f"--Role: {n['user'].get('role')} | href='{target_url}'")
            print(f"--PK: {n['user'].get('publicKey')} | href='{target_url}'")

        #
        # Metrics menu
        #
        if n.get("deviceMetrics"):
            uptime = int(n["deviceMetrics"].get("uptimeSeconds", 0))
            uptime_days, uptime_hours, uptime_minutes, uptime_seconds = seconds_to_dhms(
                uptime
            )

            print("-----")
            print(f"--{icon['pager']} Device")

            print(
                f"--Battery: {n['deviceMetrics'].get('batteryLevel', None)}% | href='{target_url}'"
            )

            print(
                f"--Voltage: {n['deviceMetrics'].get('voltage', None)} | href='{target_url}'"
            )
            print(
                f"--Channel Util: {n['deviceMetrics'].get('channelUtilization')} | href='{target_url}'"
            )
            print(
                f"--Air Util: {n['deviceMetrics'].get('airUtilization')} | href='{target_url}'"
            )
            print(
                f"--Uptime: {uptime_days}d {uptime_hours}h {uptime_minutes}m {uptime_seconds}s| href='{target_url}'"
            )
            print(f"--Seconds: {uptime}| href='{target_url}'")

        #
        # Position menu
        #
        if n.get("position"):
            print("-----")
            print(f"--{icon['globe_america']} Position")
            # TODO copy latlon to buffer for copypasta when clicked
            print(f"--Latitude: {n['position'].get('latitude')} | href='{target_url}'")
            print(
                f"--Longitude: {n['position'].get('longitude')} | href='{target_url}'"
            )
            print(f"--Altitude: {n['position'].get('altitude')} | href='{target_url}'")
            print(
                f"--Source: {n['position'].get('locationSource')} | href='{target_url}'"
            )

            if n["position"].get("time"):
                pos_time = n["position"].get("time")
                print(
                    f"--Time: {dt.datetime.fromtimestamp(pos_time)} | href='{target_url}'"
                )

            #
            # Maps menu
            #
            print("--Open In...")
            print(
                "----Open Street Maps | href='https://www.openstreetmap.org/?mlat={}&mlon={}'".format(
                    n["position"].get("latitude"),
                    n["position"].get("longitude"),
                )
            )
            print(
                "----Apple Maps | href='https://maps.apple.com/map?ll={},{}'".format(
                    n["position"].get("latitude"),
                    n["position"].get("longitude"),
                )
            )
            print(
                "----Waze | href='https://www.waze.com/ul?ll={}%2C{}&navigate=yes&zoom=17'".format(
                    n["position"].get("latitude"),
                    n["position"].get("longitude"),
                )
            )
            print(
                "----Google Maps | href='https://www.google.com/maps/search/?api=1&query={}%2C{}'".format(
                    n["position"].get("latitude"),
                    n["position"].get("longitude"),
                )
            )
            print(
                "----Google Drive | href='https://www.google.com/maps/dir/?api=1&origin=&destination={}%2C{}&travelmode=walking'".format(
                    n["position"].get("latitude"),
                    n["position"].get("longitude"),
                )
            )

            # NOTE 804.67 meters = 0.5 mile
            print(
                "----Free Map | href='https://www.freemaptools.com/radius-around-point.htm?lat={}&lng={}&r=804.67'".format(
                    n["position"].get("latitude"),
                    n["position"].get("longitude"),
                )
            )
            print(
                "----Bing Maps | href='https://bing.com/maps/default.aspx?cp={}~{}&lvl=14'".format(
                    n["position"].get("latitude"),
                    n["position"].get("longitude"),
                )
            )

        #
        # Comms menu
        #
        print("-----")
        print(f"--{icon['satellite']} Comms")

        # HACK the node id starts with ! which is being interpreted by the shell, need to escape them, vscode is eating this on save somehow https://github.com/swiftbar/SwiftBar/issues/308
        if config["bitbar"] == "xbar":
            node_escaped = node.replace("!", r"\!")
        if config["bitbar"] == "swiftbar":
            node_escaped = node
        if config["bitbar"] == "argos":
            # TODO unknown shell escape behavior in argos
            node_escaped = node
        if config["bitbar"] == "local":
            node_escaped = node.replace("!", r"\!")

        print(
            f"--Traceroute | {SHELL}='meshtastic' {B} terminal=true {B} param1={config['meshtastic_p1']} {B} param2={config['meshtastic_p2']} {B} param3='--traceroute' {B} param4='{node_escaped}' {B} param5='|' {B} param6='tee {config['log_dir']}/{config['log_traceroute_log']}'"
        )

        print("--Request")
        print(
            f"----Request position | {SHELL}='meshtastic' {B} terminal=true {B} param1={config['meshtastic_p1']} {B} param2={config['meshtastic_p2']} {B} param3='--request-position' {B} param4='--dest' {B} param5='{node_escaped}'"
        )

        print("----Telemetry")
        for telemetry_type in telemetry_types:
            print(
                f"----{telemetry_type} | {SHELL}='meshtastic' {B} terminal=true {B} param1={config['meshtastic_p1']} {B} param2={config['meshtastic_p2']} {B} param3='--request-telemetry' {B} param4='{telemetry_type}' {B} param5='--dest' {B} param6='{node_escaped}' "
            )

        print(f"--Send text")
        for txt in txts:
            print(
                f"----{txt} | terminal=true {B} {SHELL}='meshtastic' {B} param1={config['meshtastic_p1']} {B} param2={config['meshtastic_p2']} {B} param3='--sendtext' {B} param4='{txt}' {B} param5='--dest' {B} param6='{node_escaped}'"
            )

    if config.get("log_wifi_report") and config.get("use_wifi"):
        import requests

        with open(
            f"{config['log_dir']}/{config['log_wifi_report']}",
            "a",
            encoding="utf-8",
        ) as f:
            f.write(
                json.dumps(
                    {
                        "timestamp": str(ts),
                        "report": requests.get(
                            f"{target_url}/json/report", timeout=10
                        ).json(),
                    }
                )
                + "\n"
            )

    if config.get("log_nodes_csv"):
        import csv

        def flatten_node(node):
            flat_node = {}
            for key, value in node.items():
                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        flat_node[f"{key}_{sub_key}"] = sub_value
                else:
                    flat_node[key] = value
            return flat_node

        flattened_nodes = [flatten_node(node) for node in nodes.values()]

        # sort unique keys for header so git diff is consistent
        keys = set()
        for node in flattened_nodes:
            keys.update(node.keys())
        keys = sorted(list(keys))

        with open(
            f"{config['log_dir']}/{config['log_nodes_csv']}",
            "w",
            encoding="utf-8",
        ) as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=keys)
            writer.writeheader()
            for node in flattened_nodes:
                writer.writerow(node)

    # currently 13 seconds with uv on m2, not bad when running every 5m, mostly waiting on radio
    print(f"Runtime: {dt.datetime.now() - ts}")

    # OS Error:
    #   The serial device couldn't be opened, it might be in use by another process.
    #   Please close any applications or webpages that may be using the device and try again.
    #
    # Original error: [Errno 35] Could not exclusively lock port /dev/cu.usbserial-0001: [Errno 35] Resource temporarily unavailable


if __name__ == "__main__":
    cli(load_config())
