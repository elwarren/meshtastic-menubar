#!/opt/homebrew/bin/uv run --no-project --with pytap2 --with meshtastic[cli] --python 3.12 --script
# -*- coding: utf-8 -*-
#
# Show meshtastic nodes and stats in the menubar
#
# <xbar.title>Meshtastic Menubar</xbar.title>
# <xbar.version>2025.3.7</xbar.version>
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
from sys import version as python_version

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

VERSION = "2025.3.7"


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
        "log_dir": os.environ.get("HOME"),
        "bitbar": "xbar",
        "font_mono": "Menlo-Regular",
        "interval": 5,
        "meshtastic_bin": "meshtastic",
        "meshtastic_p1": "--host",
        "meshtastic_p2": "meshtastic.local",
        "config_file": f"{os.environ.get('HOME')}/.meshtastic-menubar.yml",
        # HACK to get the shell bar separators to work in xbar and swiftbar
        "B": "|",
        "SHELL": "shell",
    }

    if os.path.exists(config["config_file"]):
        with open(config["config_file"], "r") as f:
            new_config = load(f.read(), Loader=Loader)
            config.update(new_config)

    # Maybe http saves some battery because https uses more cpu
    if config.get("use_https"):
        config["target_url"] = f"https://{config.get('wifi_host')}"
    else:
        config["target_url"] = f"http://{config.get('wifi_host')}"

    return config


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


def print_menu_icon(menu_status: str = None, menu_icon: str = None):
    """Display icon atop menubar. Optionally accepts a status text to show next to M icon."""

    if menu_icon is None:
        # base64 encoded image of Meshtastic logo
        menu_icon = "iVBORw0KGgoAAAANSUhEUgAAADIAAAAcCAYAAAAjmez3AAAACXBIWXMAAA7DAAAOwwHHb6hkAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAApZJREFUWIXtmE2ITWEYx38zjvFthiFfC5OFaCZFJE2RRCIlysJuFGUxiVkYiylFmWxYTBGbWY2PUhJlwyyFSPmIhOQrYyjEmOHeY3Hcuce5/zPnOfe8d6H86yzuvc/vef7nve857/O+8F8AjAJ2AzUZctQB1W7slK92wAfuA4tTsjXAOSAP9AEr3Vqzqwn4QXAjPjAIHACqjHxniPWBD8BM9zZHlgfcjhjxgTNGfgXwS/CXnDtN0CFh4i1Qb2DHA08EX7haKuBXagkwJAxsNPJdgg1fn4G5bi2XagzwQBQ/beTXEDzcYTb62QeuU+E32TFR9AUw2cDWAi8Fv4PgrRf9fo9j78NqBnKRYjlgtZHvptTsxT+/qek6ADS6sV7UBOCpMHLcyG8SbB8wIxRzUMTcAUZndh/SKVHkMTDOwE4D3gl+ayTOA26JuI7s9gOtpfSB/AksN/LnhbnumNiFwHdRa1l51ouqA14JI4eN/HbBvgamjMC0CeYRMDa9/aJ6RNJ72JrE2cDHCJsH1idw1UCvqHs0vf1Am0WyQWCRkb8i+C4j2wB8ibA5YJWRH9Z04L0w0m7kdwn2GTAxhYedIsdzYFKKHFwQSW4Q7D+S1IAezXLa9MvCx0kr3CLgb8B8Axs3vzvt3v/SLKA/kisPbEgC5wCfhJFWY+F9gn1ItjfOFpHzDTA1DqgCrgroGrbN0gL0GrC03DsI6azw1RMX3CqCrS21B9wUvKtVOW492xYNnAd8FYHWTU6HYF33Seso7TD6iWyPTwgj1m1nPaWDMEDQbriW6vmOhAM8YD/Fw4S0BwGNBP9AIfnezJa1wl34EEHHLJeEJuAuYu4ZVBiM3rjkjtRM0CYlHj95GQtV8iYKsh45/Xv6DTfbUnnkjAuSAAAAAElFTkSuQmCC"

    if menu_status:
        print(f"{menu_status} | templateImage='{menu_icon}'")
    else:
        print(f" | templateImage='{menu_icon}'")

    print("---")


def print_menu_bar(depth: int = 0):
    """Display Meshtastic Menubar submenu"""
    print(menu_line(f"Meshtastic Menubar", depth))


def print_menu_about(depth: int = 1):
    """Display About submenu"""
    print(menu_line(f"{icon['waffle']} About", depth))
    print(menu_line(f"Meshtastic Menubar | href={git_repo_url}", depth=depth + 1))
    print(menu_line(f"Version: {VERSION} | href={git_zip_url}", depth=depth + 1))

    print(menu_line("---", depth=depth + 1))

    print(menu_line("Built with:", depth=depth + 1))
    print(
        menu_line(f"Meshtastic Project | href={meshtastic_home_url}", depth=depth + 1)
    )
    print(menu_line(f"Meshtastic Python | href={meshtastic_repo_url}", depth=depth + 1))
    print(menu_line(f"xbar (bitbar) | href={xbar_repo_url}", depth=depth + 1))
    print(menu_line(f"Swiftbar | href={swiftbar_repo_url}", depth=depth + 1))
    print(menu_line(f"Argos | href={argos_repo_url}", depth=depth + 1))


def print_menu_refresh(depth: int = 1):
    """Display Refresh submenu"""
    print(menu_line("---", depth))
    print(menu_line(f"{icon['refresh']} Refresh | refresh=true", depth))


def print_menu_broadcast(depth: int = 1):
    """Display node Broadcast submenu"""
    print(menu_line(f"{icon['satellite']} Broadcast", depth))

    for txt in txts:
        # TODO new machine has different setup than my build machine. zsh: command not found: meshtastic
        # TODO i hate shell escaping in these apps
        # "meshtastic.local" 'meshtastic' --port /dev/cu.usbserial-0001 --sendtext What up?
        # zsh: no matches found: up?
        print(
            menu_line(
                f"{txt} | {config['SHELL']}='meshtastic' {config['B']} terminal=true {config['B']} param1={config['meshtastic_p1']} {config['B']} param2={config['meshtastic_p2']} {config['B']} param3='--sendtext' {config['B']} param4='{txt}'",
                depth=depth + 1,
            )
        )


def print_menu_device(depth: int = 1):
    """Display host Device submenu"""

    print(menu_line(f"{icon['gear']} Device", depth))
    print(
        menu_line(
            f"Reboot | {config['SHELL']}='meshtastic' {config['B']} terminal=true {config['B']} param1={config['meshtastic_p1']} {config['B']} param2={config['meshtastic_p2']} {config['B']}param3='--reboot'",
            depth=depth + 1,
        )
    )
    print(
        menu_line(
            f"Shutdown | {config['SHELL']}='meshtastic' {config['B']} terminal=true {config['B']} param1={config['meshtastic_p1']} {config['B']} param2={config['meshtastic_p2']} {config['B']}param3='--shutdown'",
            depth=depth + 1,
        )
    )
    print(
        menu_line(
            f"Tail logs | {config['SHELL']}='meshtastic' {config['B']} terminal=true {config['B']} param1={config['meshtastic_p1']} {config['B']} param2={config['meshtastic_p2']} {config['B']}param3='--noproto'",
            depth=depth + 1,
        )
    )
    print(
        menu_line(
            f"BLE Scan | {config['SHELL']}='meshtastic' {config['B']} terminal=true {config['B']} param1={config['meshtastic_p1']} {config['B']} param2={config['meshtastic_p2']} {config['B']}param3='--ble-scan'",
            depth=depth + 1,
        )
    )
    print(
        menu_line(
            f"json Report | {config['SHELL']}='open' {config['B']} terminal=false {config['B']} param1='{config['target_url']}/json/report'",
            depth=depth + 1,
        )
    )


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
            f"Edit Config File: {config['config_file']} | shell='vi' | terminal=true | param1={config['config_file']}",
            depth=depth + 1,
        )
    )

    for param in sorted(config):
        print(menu_line(f"{param}={config[param]}", depth=depth + 1))


def print_menu_versions(depth: int = 1):
    """Show package versions submenu"""

    print(menu_line("Versions", depth))
    print(menu_line(f"Python: {python_version}", depth=depth + 1))
    print(
        menu_line(
            f"Meshtastic: {meshtastic.version.get_active_version()}", depth=depth + 1
        )
    )


def print_menu_help(depth: int = 1):
    """Show Help submenu"""

    print(menu_line("---", depth))
    print(menu_line(f"{icon['question']} Help", depth))

    print(menu_line("🟢 Green nodes have been heard in past hour", depth=depth + 1))
    print(menu_line("🟡 Yellow nodes three hours", depth=depth + 1))
    print(menu_line("🟠 Orange 12 hours", depth=depth + 1))
    print(menu_line("🔴 Red past three days", depth=depth + 1))
    print(menu_line("🟣 Purple heard in past seven days", depth=depth + 1))
    print(
        menu_line(
            "🔵 Blue nodes are ice cold, we haven't heard from them in over a week",
            depth=depth + 1,
        )
    )
    print(
        menu_line(
            "⚫ Black nodes were partially received without timestamp", depth=depth + 1
        )
    )
    print(menu_line("---", depth=depth + 1))
    print(menu_line(f"📚 RTFM | href='{git_repo_url}'", depth=depth + 1))


def print_menu_node_heard(
    n,
    status_icon,
    heard_str,
    heard_ago,
    heard_ago_total_seconds,
    heard_at_dt,
    heard_last,
):
    """Display node Heard submenu"""
    print(f"--{icon['satdish']} Heard")
    print(f"--SNR: {n.get('snr')} | href='{config['target_url']}'")
    print(f"--Hops away: {n.get('hopsAway')} | href='{config['target_url']}'")
    print(f"--Last: {heard_str}| href='{config['target_url']}'")
    print(f"--Seconds: {heard_ago_total_seconds}| href='{config['target_url']}'")
    print(f"--DT: {heard_at_dt}| href='{config['target_url']}'")
    # print(f"--Epoc: {heard_last}| href='{config['target_url']}'")


def print_menu_node_device(n):
    """Display node Device submenu"""
    uptime = int(n["deviceMetrics"].get("uptimeSeconds", 0))
    uptime_days, uptime_hours, uptime_minutes, uptime_seconds = seconds_to_dhms(uptime)

    print("-----")
    print(f"--{icon['pager']} Device")

    print(
        f"--Battery: {n['deviceMetrics'].get('batteryLevel', None)}% | href='{config['target_url']}'"
    )

    print(
        f"--Voltage: {n['deviceMetrics'].get('voltage', None)} | href='{config['target_url']}'"
    )
    print(
        f"--Channel Util: {n['deviceMetrics'].get('channelUtilization')} | href='{config['target_url']}'"
    )
    print(
        f"--Air Util: {n['deviceMetrics'].get('airUtilization')} | href='{config['target_url']}'"
    )
    print(
        f"--Uptime: {uptime_days}d {uptime_hours}h {uptime_minutes}m {uptime_seconds}s| href='{config['target_url']}'"
    )
    print(f"--Seconds: {uptime}| href='{config['target_url']}'")


def print_menu_node_user(n):
    """Display node User submenu"""
    print("-----")
    print(f"--{icon['ticket']} User")
    print(f"--Name: {n['user'].get('longName')} | href='{config['target_url']}'")
    print(f"--Short: {n['user'].get('shortName')} | href='{config['target_url']}'")
    print(f"--Model: {n['user'].get('hwModel')} | href='{config['target_url']}'")
    print(f"--Role: {n['user'].get('role')} | href='{config['target_url']}'")
    print(f"--PK: {n['user'].get('publicKey')} | href='{config['target_url']}'")


def print_menu_node_position(n):
    """Display node Position submenu"""

    print("-----")
    print(f"--{icon['globe_america']} Position")
    # TODO copy latlon to buffer for copypasta when clicked
    print(
        f"--Latitude: {n['position'].get('latitude')} | href='{config['target_url']}'"
    )
    print(
        f"--Longitude: {n['position'].get('longitude')} | href='{config['target_url']}'"
    )
    print(
        f"--Altitude: {n['position'].get('altitude')} | href='{config['target_url']}'"
    )
    print(
        f"--Source: {n['position'].get('locationSource')} | href='{config['target_url']}'"
    )

    if n["position"].get("time"):
        pos_time = n["position"].get("time")
        print(
            f"--Time: {dt.datetime.fromtimestamp(pos_time)} | href='{config['target_url']}'"
        )

    #
    # Maps submenu
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


def print_menu_node_comms(node):
    """Display node Comms submenu"""

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
        f"--Traceroute | {config['SHELL']}='meshtastic' {config['B']} terminal=true {config['B']} param1={config['meshtastic_p1']} {config['B']} param2={config['meshtastic_p2']} {config['B']} param3='--traceroute' {config['B']} param4='{node_escaped}' {config['B']} param5='|' {config['B']} param6='tee {config['log_dir']}/{config['log_traceroute_log']}'"
    )

    print("--Request")
    print(
        f"----Request position | {config['SHELL']}='meshtastic' {config['B']} terminal=true {config['B']} param1={config['meshtastic_p1']} {config['B']} param2={config['meshtastic_p2']} {config['B']} param3='--request-position' {config['B']} param4='--dest' {config['B']} param5='{node_escaped}'"
    )

    print("----Telemetry")
    for telemetry_type in telemetry_types:
        print(
            f"----{telemetry_type} | {config['SHELL']}='meshtastic' {config['B']} terminal=true {config['B']} param1={config['meshtastic_p1']} {config['B']} param2={config['meshtastic_p2']} {config['B']} param3='--request-telemetry' {config['B']} param4='{telemetry_type}' {config['B']} param5='--dest' {config['B']} param6='{node_escaped}' "
        )

    print(f"--Send text")
    for txt in txts:
        print(
            f"----{txt} | terminal=true {config['B']} {config['SHELL']}='meshtastic' {config['B']} param1={config['meshtastic_p1']} {config['B']} param2={config['meshtastic_p2']} {config['B']} param3='--sendtext' {config['B']} param4='{txt}' {config['B']} param5='--dest' {config['B']} param6='{node_escaped}'"
        )


def get_node_short_name(n):
    # have to reach into potentially missing keys to build main menu
    try:
        return n["user"].get("shortName")
    except:
        return None


def get_node_hops_icon(n):
    # have to reach into potentially missing keys to build main menu
    if n.get("hopsAway") == 0:
        return icon["zero"]
    elif n.get("hopsAway") == 1:
        return icon["one"]
    elif n.get("hopsAway") == 2:
        return icon["two"]
    elif n.get("hopsAway") == 3:
        return icon["three"]
    elif n.get("hopsAway") == 4:
        return icon["four"]
    elif n.get("hopsAway") == 5:
        return icon["five"]
    elif n.get("hopsAway") == 6:
        return icon["six"]
    elif n.get("hopsAway") == 7:
        return icon["seven"]
    elif n.get("hopsAway") == 8:
        return icon["eight"]
    elif n.get("hopsAway") == 9:
        return icon["nine"]
    else:
        return icon["star"]


def calculate_heards(heard_last=None):
    # if heard_last is None then black because we can't calculate time without it
    status_icon = icon["black"]
    heard_str = "Not Reported"
    heard_ago = None
    heard_ago_total_seconds = None
    heard_at_dt = None
    # heard_last = n.get("lastHeard")

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

        heard_str = f"{heard_days}d {heard_hours}h {heard_minutes}m {heard_seconds}s"

    return (
        status_icon,
        heard_str,
        heard_ago,
        heard_ago_total_seconds,
        heard_at_dt,
        heard_last,
    )


def print_menu_nodes(nodes):
    """Display all Nodes and their submenus"""

    # NOTE default lastHeard to zero because relayed nodes do not report and we need this to sort
    nodelist = sorted(nodes, reverse=True, key=lambda x: nodes[x].get("lastHeard", 0))
    print("---")
    print(f"Nodes: {len(nodelist)}")

    first_node = True
    for id in nodelist:
        node = nodes[id]

        (
            status_icon,
            heard_str,
            heard_ago,
            heard_ago_total_seconds,
            heard_at_dt,
            heard_last,
        ) = calculate_heards(heard_last=node.get("lastHeard"))

        #
        # First line is always our node so it gets a special mesh icon
        #
        if first_node:
            first_node = False
            print(
                f"{icon['globe_mesh']} {id} {icon['hash']} {get_node_short_name(node)} | font={config['font_mono']}"
            )
        else:
            print(
                f"{status_icon} {id} {get_node_hops_icon(node)} {get_node_short_name(node)} | font={config['font_mono']}"
            )

        #
        # First submenu
        #
        # Heard submenu
        #
        print_menu_node_heard(
            node,
            status_icon,
            heard_str,
            heard_ago,
            heard_ago_total_seconds,
            heard_at_dt,
            heard_last,
        )

        #
        # User submenu
        #
        if node.get("user"):
            print_menu_node_user(node)

        #
        # Metrics menu
        #
        if node.get("deviceMetrics"):
            print_menu_node_device(node)

        #
        # Position menu
        #
        if node.get("position"):
            print_menu_node_position(node)

        #
        # Comms menu
        #
        print_menu_node_comms(id)


git_repo_url = "https://github.com/elwarren/meshtastic-menubar"
git_zip_url = f"{git_repo_url}/archive/refs/heads/master.zip"
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
    "zero": "0️⃣",
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


def cli(config: dict):
    """This is __main__ code when called as cli vs testing."""

    #
    # show menu bar icon asap so that if we throw exception we still have a menu
    #
    print_menu_icon()

    no_device = False
    test_empty = False

    #
    # get meshtastic interface depending on connection type
    #
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
            config["meshtastic_p2"] = config.get("wifi_host")
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
        # fail fast if device doesn't exist or path incorrect
        serial_fail = False
        if config.get("serial_port"):
            if os.path.exists(config.get("serial_port")):

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
                    serial_fail = True
                    # TODO Exception connecting via Serial: [Errno 35] Could not exclusively lock port /dev/cu.usbserial-0001: [Errno 35] Resource temporarily unavailable

            else:
                serial_fail = True
        else:
            serial_fail = True

        if serial_fail:
            print(f"Serial device does not exist at: {config.get('serial_port')}")
            no_device = "No connection method set"
            print_menu_debug(depth=0)
            print_menu_environment(depth=1)
            print_menu_config(config, depth=1)
            # should we exit 0 or 1? how does xbar handle this vs swiftbar?
            exit(0)

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

    #
    # main menu display output
    #
    print_menu_bar(depth=0)

    #
    # menu drop down begin
    #
    print_menu_about(depth=1)
    print_menu_refresh(depth=1)
    print_menu_broadcast(depth=1)
    print_menu_device(depth=1)

    print_menu_debug(depth=1)
    print_menu_environment(depth=2)
    print_menu_config(config, depth=2)
    # print_menu_nodelist(nodelist, depth=2)
    print_menu_versions(depth=2)

    print_menu_help(depth=1)

    #
    # back to main menu again
    #
    print(f"Every: {config['interval']}m Last Run:")
    print(f"{ts.replace(microsecond=0)}")
    print("---")

    # bail out if no nodes nothing to show
    if test_empty or no_device or len(nodes) < 1:
        print(f"{icon['police']} No Device or Nodes!")
        # show no_device holds our exception text
        print(no_device)
        exit(0)

    print_menu_nodes(nodes)
    #
    # End nodes submenu
    #

    #
    # Final act
    #
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
                            f"{config['target_url']}/json/report", timeout=10
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
    config = load_config()
    cli(config)
