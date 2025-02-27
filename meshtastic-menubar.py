#!/opt/homebrew/bin/uv run --python 3.12 --script
# TODO env can't find uv on macos #!/usr/bin/env -S uv run --script
# -*- coding: utf-8 -*-
#
# Shows meshtastic node info in your menu bar on macos or linux
#
# /// script
# requires-python = ">=3.12"
# dependencies = [
# "pytap2",
# "requests",
# "meshtastic[cli]",
# ]
# ///
#
# <xbar.title>Meshtastic Menubar</xbar.title>
# <xbar.version>v0.4</xbar.version>
# <xbar.author>elwarren</xbar.author>
# <xbar.author.github>elwarren</xbar.author.github>
# <xbar.desc>Get nodelist and stats from Meshtastic device.</xbar.desc>
# <xbar.dependencies>python,uv,meshtastic</xbar.dependencies>
# <xbar.abouturl>https://github.com/elwarren/meshtastic-menubar</xbar.abouturl>
#
# Default configuration to be overridden by xbar
# NOTE these don't seem to be supported by swiftbar
# TODO create a config file, all this environment parsing is stupid and doesn't work consistently
#
# <xbar.var>select(VAR_CONNECTION="wifi"): How to connect to device. [wifi, bluetooth, serial]</xbar.var>
# <xbar.var>string(VAR_WIFI_HOST="meshtastic.local"): Hostname if using wifi</xbar.var>
# <xbar.var>string(VAR_BLUETOOTH_NAME="YOUR_NODE"): BLE node name if using bluetooth</xbar.var>
#
# NOTE this is different across boards, cables, systems
# <xbar.var>string(VAR_SERIAL_PORT="/dev/ttyUSB0"): Path to USB device if using serial</xbar.var>
#
# <xbar.var>boolean(VAR_LOG_JSON=true): Write line delimited json file of nodes</xbar.var>
# <xbar.var>boolean(VAR_LOG_CSV=true): Write CSV file of nodes</xbar.var>
# <xbar.var>boolean(VAR_LOG_REPORT=true): Fetch status report from node</xbar.var>
#
# <xbar.var>string(VAR_LOG_DIR="/Users/yourname/Meshtastic"): Directory to write logs</xbar.var>
#

import os
import datetime as dt
import json

import meshtastic

ts = dt.datetime.now()

# if there's no config then default to wifi
is_xbar = False
is_swiftbar = False
is_argos = False
is_local = True
use_wifi = False
use_serial = False
use_bt = False
wifi_host = "meshtastic.local"
bluetooth_name = "YOUR_NODE"
serial_port = "/dev/ttyUSB0"
interval = 5
VERSION = "v0.4"
# HACK to get the shell bar separators to work in xbar and swiftbar
B = "|"
SHELL = "shell"

if os.environ.get("VAR_CONNECTION"):
    # Currently only xbar sets VAR_CONNECTION and XBARDarkMode
    is_xbar = True
    is_local = False
    interval = int(os.environ.get("VAR_INTERVAL"))
elif os.environ.get("SWIFTBAR_VERSION"):
    # Swiftbar does not set VAR_CONNECTION
    is_swiftbar = True
    is_local = False
    use_wifi = True
    os.environ.setdefault("VAR_CONNECTION", "wifi")
    # swiftbar wants params to be in the shell command without bar separators
    B = ""
    SHELL = "bash"
elif os.environ.get("ARGOS_VERSION"):
    # TODO argos completely untested
    # https://github.com/p-e-w/argos?tab=readme-ov-file#environment-variables
    is_argos = True
    is_local = False
    use_wifi = True
    os.environ.setdefault("VAR_CONNECTION", "wifi")
    # TODO argos bar separator behavior uknown
    B = ""
else:
    # must be local testing if we don't have xbar or swiftbar
    use_wifi = True
    os.environ.setdefault("VAR_CONNECTION", "wifi")

# TODO swiftbar doesn't support these
if use_wifi or os.environ.get("VAR_CONNECTION") == "wifi":
    use_wifi = True
    if os.environ.get("VAR_WIFI_HOST"):
        wifi_host = os.environ.get("VAR_WIFI_HOST")

if use_serial or os.environ.get("VAR_CONNECTION") == "serial":
    use_serial = True
    if os.environ.get("VAR_SERIAL_PORT"):
        serial_port = os.environ.get("VAR_SERIAL_PORT")

if use_bt or os.environ.get("VAR_CONNECTION") == "bluetooth":
    use_bt = True
    if os.environ.get("VAR_BLUETOOTH_NAME"):
        bluetooth_name = os.environ.get("VAR_BLUETOOTH_NAME")

# Log output to files or leave filesystem alone?
logdir = os.path.expanduser("~")
log_nodes = True
log_nodes_jsonl = ".meshtastic-menubar.nodes.jsonl"
log_report = True
log_wifi_report = ".meshtastic-menubar.report.json"
log_csv = True
log_nodes_csv = ".meshtastic-menubar.nodes.csv"
log_traceroute = True
log_traceroute_log = ".meshtastic-menubar.traceroute.log"

# Display output with monospaced font to align columns
font_mono = "Monaco"
# TODO accept command line params
no_device = False
test_empty = False
# debug will get nodes and exit
debug = False

# Maybe http saves some battery because https uses more cpu
target_url = f"http://{wifi_host}"
git_home_url = "https://github.com/elwarren/"
git_repo_url = "https://github.com/elwarren/meshtastic-menubar"
git_zip_url = "https://github.com/meshtastic/python/archive/refs/heads/master.zip"
meshtastic_home_url = "https://meshtastic.org/"
meshtastic_repo_url = "https://github.com/meshtastic/python/"
xbar_repo_url = "https://github.com/matryer/xbar/"
swiftbar_repo_url = "https://github.com/swiftbar/SwiftBar/"
argos_repo_url = "https://github.com/p-e-w/argos"

# icons to choose from
icon_green = "🟢"
icon_yellow = "🟡"
icon_orange = "🟠"
icon_red = "🔴"
icon_blue = "🔵"
icon_purple = "🟣"
icon_brown = "🟤"
icon_black = "⚫"
icon_white = "⚪"
icon_police = "🚨"
icon_ticket = "🎫"
icon_person = "👤"
icon_people = "👥"
icon_voltage = "⚡"
icon_battery = "🔋"
icon_battery_low = "🪫"
icon_plug = "🔌"
icon_pager = "📟"
icon_satdish = "📡"
icon_satellite = "🛰️"
icon_telescope = "🔭"
icon_bars = "📶"
icon_hash = "#️⃣"
icon_star = "*️⃣"
icon_one = "1️⃣"
icon_two = "2️⃣"
icon_three = "3️⃣"
icon_four = "4️⃣"
icon_five = "5️⃣"
icon_six = "6️⃣"
icon_seven = "7️⃣"
icon_eight = "8️⃣"
icon_nine = "9️⃣"
icon_globe_mesh = "🌐"
icon_globe_america = "🌎"
icon_compass = "🧭"
icon_tent = "⛺"
icon_office = "🏢"
icon_house = "🏠"
icon_gear = "⚙️"
icon_settings = "⚙️"
icon_trash = "🗑️"
icon_about = "🆎"
icon_question = "❓"
icon_exclaim = "❗"
icon_refresh = "🔄"
icon_waffle = "🧇"
icon_pancakes = "🥞"
icon_wave = "👋"
icon_thumbsup = "👍"
icon_thumbsdown = "👎"
icon_victory = "✌️"
icon_horns = "🤘"
icon_ok_hand = "👌"
icon_ok_button = "🆗"
icon_prohibited = "🚫"
icon_one_hundred = "💯"

# TODO what are valid telemetry types?
telemetry_types = [
    "gps",
    "battery",
    "position",
    "user",
    "device",
]

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
    icon_wave,
    icon_thumbsup,
    icon_thumbsdown,
    icon_victory,
    icon_horns,
    icon_ok_hand,
    icon_prohibited,
    icon_one_hundred,
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

# show menu bar icon asap so that if we throw exception we still have a menu
print(f" | templateImage='{menu_icon}'")
print("---")


def seconds_to_dhms(seconds: int) -> tuple[int, int, int, int]:
    """Compute days, hours, minutes, seconds from total seconds"""

    days = seconds // (24 * 3600)
    remaining_seconds = seconds % (24 * 3600)

    hours = remaining_seconds // 3600
    remaining_seconds = remaining_seconds % 3600

    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60

    return days, hours, minutes, seconds


iface = None
if use_wifi:
    # TODO is importing late bad style? Trying to reduce imports and speed startup
    try:
        import meshtastic.tcp_interface  # as miw

        iface = meshtastic.tcp_interface.TCPInterface(hostname=wifi_host)
        meshtastic_bin = f"meshtastic --host {wifi_host}"
        meshtastic_p1 = "--host"
        meshtastic_p2 = wifi_host
    except Exception as e:
        print(f"Exception connecting via Wifi: {e}")
        no_device = str(e)
elif use_bt:
    try:
        import meshtastic.ble_interface  # as mib

        iface = meshtastic.ble_interface.BLEInterface(address=bluetooth_name)
        meshtastic_bin = f"meshtastic --ble {bluetooth_name}"
    except Exception as e:
        print(f"Exception connecting via Bluetooth: {e}")
        no_device = str(e)
elif use_serial:
    try:
        import meshtastic.serial_interface  # as mis

        iface = meshtastic.serial_interface.SerialInterface()
        meshtastic_bin = f"meshtastic --port {serial_port}"
    except Exception as e:
        print(f"Exception connecting via Serial: {e}")
        no_device = str(e)
else:
    print("No connection method set")
    print("Set VAR_CONNECTION to wifi, bluetooth, or serial")
    no_device = "No connection method set"
    # should we exit 0 or 1? how does xbar handle this vs swiftbar?
    exit(0)

# TODO above should avoid iface.nodes exception but need to test
#     nodes = dict(iface.nodes)
#                  ^^^^^^^^^^^
# AttributeError: 'NoneType' object has no attribute 'nodes'

nodes = dict(iface.nodes)
iface.close()

# log nodes early incase we are debugging and skip gui
if log_nodes:
    with open(f"{logdir}/{log_nodes_jsonl}", "a", encoding="utf-8") as f:
        f.write(json.dumps({"timestamp": str(ts), "nodes": nodes}) + "\n")

if debug:
    print("Environment:\n", json.dumps(os.environ))
    print("Nodes:\n", json.dumps(dict(nodes)))
    exit(0)

nodelist = []
if no_device:
    pass
else:
    # NOTE default lastHeard to zero because relayed nodes do not report and we need this to sort
    nodelist = sorted(nodes, reverse=True, key=lambda x: nodes[x].get("lastHeard", 0))

#
# main menu display output
#
# menu drop down begin
#
print(f"Meshtastic Menubar")

print("-----")
print(f"--{icon_waffle} About")
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
print(f"--{icon_refresh} Refresh | refresh=true")

print(f"--{icon_satellite} Broadcast")

# TODO might need to escape these for shell
for txt in txts:
    print(
        f"----{txt} | {SHELL}='meshtastic' {B} terminal=true {B} param1={meshtastic_p1} {B} param2={meshtastic_p2} {B} param3='--sendtext' {B} param4='{txt}'"
    )

print(f"--{icon_gear} Device")
print(
    f"----Reboot | {SHELL}='meshtastic' {B} terminal=true {B} param1={meshtastic_p1} {B} param2={meshtastic_p2} {B}param3='--reboot'"
)
print(
    f"----Shutdown | {SHELL}='meshtastic' {B} terminal=true {B} param1={meshtastic_p1} {B} param2={meshtastic_p2} {B}param3='--shutdown'"
)
print(
    f"----Tail logs | {SHELL}='meshtastic' {B} terminal=true {B} param1={meshtastic_p1} {B} param2={meshtastic_p2} {B}param3='--noproto'"
)
print(
    f"----BLE Scan | {SHELL}='meshtastic' {B} terminal=true {B} param1={meshtastic_p1} {B} param2={meshtastic_p2} {B}param3='--ble-scan'"
)
print(
    f"----json Report | {SHELL}='open' {B} terminal=false {B} param1='{target_url}/json/report'"
)
print(f"--{icon_exclaim} Debug")
print("----Environment:")
for var in os.environ:
    print(f"----{var}={os.environ[var]}")


print("-----")
print(f"--{icon_question} Help")
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
print(f"Every: {interval}m Last Run:")
print(f"{ts.replace(microsecond=0)}")
print("---")

# bail out if no nodes nothing to show
if test_empty or no_device or len(nodelist) < 0:
    print(f"{icon_police} No Device or Nodes!")
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
    status_icon = icon_black
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

        if debug:
            print(
                f"heard_ago {heard_ago} = now {ts} - heard_at_dt {heard_at_dt} heard_ago_seconds {heard_ago_total_seconds}"
            )

        # blue is on ice because it's been over a week since we heard from them
        status_icon = icon_blue

        # purple if heard in last week
        if heard_days < 8:
            status_icon = icon_purple

        # red if heard in last 3 days
        if heard_days < 4:
            status_icon = icon_red

        # orange if heard in last 12 hours 43200 sec
        if heard_ago_total_seconds < (12 * 60 * 60):
            status_icon = icon_orange

        # yellow if heard in last three hours 10800 sec
        if heard_ago_total_seconds < (3 * 60 * 60):
            status_icon = icon_yellow

        # green if heard in last hour 3600 sec
        if heard_ago_total_seconds < (1 * 60 * 60):
            status_icon = icon_green

        heard_str = f"{heard_days}d {heard_hours}h {heard_minutes}m {heard_seconds}s"

    #
    # First line is always our node so it gets a special mesh icon
    #
    if first_node:
        first_node = False
        print(f"{icon_globe_mesh} {node} - {_name_short} | font={font_mono}")
    else:
        print(f"{status_icon} {node} - {_name_short} | font={font_mono}")

    #
    # First submenu
    #
    # Heard submenu
    #
    print(f"--{icon_satdish} Heard")
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
        print(f"--{icon_ticket} User")
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
        print(f"--{icon_pager} Device")

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
        print(f"--{icon_globe_america} Position")
        # TODO copy latlon to buffer for copypasta when clicked
        print(f"--Latitude: {n['position'].get('latitude')} | href='{target_url}'")
        print(f"--Longitude: {n['position'].get('longitude')} | href='{target_url}'")
        print(f"--Altitude: {n['position'].get('altitude')} | href='{target_url}'")
        print(f"--Source: {n['position'].get('locationSource')} | href='{target_url}'")

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
    print(f"--{icon_satellite} Comms")

    # HACK the node id starts with ! which is being interpreted by the shell, need to escape them, vscode is eating this on save somehow https://github.com/swiftbar/SwiftBar/issues/308
    if is_xbar:
        node_escaped = node.replace("!", r"\!")
    if is_swiftbar:
        node_escaped = node
    if is_argos:
        # TODO unknown shell escape behavior in argos
        node_escaped = node
    if is_local:
        node_escaped = node.replace("!", r"\!")

    print(
        f"--Traceroute | {SHELL}='meshtastic' {B} terminal=true {B} param1={meshtastic_p1} {B} param2={meshtastic_p2} {B} param3='--traceroute' {B} param4='{node_escaped}'"
    )

    print("--Request")
    print(
        f"----Request position | {SHELL}='meshtastic' {B} terminal=true {B} param1={meshtastic_p1} {B} param2={meshtastic_p2} {B} param3='--request-position' {B} param4='--dest' {B} param5='{node_escaped}'"
    )

    print("----Telemetry")
    for telemetry_type in telemetry_types:
        print(
            f"----{telemetry_type} | {SHELL}='meshtastic' {B} terminal=true {B} param1={meshtastic_p1} {B} param2={meshtastic_p2} {B} param3='--request-telemetry' {B} param4='{telemetry_type}' {B} param5='--dest' {B} param6='{node_escaped}' "
        )

    print(f"--Send text")
    for txt in txts:
        print(
            f"----{txt} | terminal=true {B} {SHELL}='meshtastic' {B} param1={meshtastic_p1} {B} param2={meshtastic_p2} {B} param3='--sendtext' {B} param4='{txt}' {B} param5='--dest' {B} param6='{node_escaped}'"
        )

if log_report:
    import requests

    with open(f"{logdir}/{log_wifi_report}", "a", encoding="utf-8") as f:
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

if log_csv:
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

    with open(f"{logdir}/{log_nodes_csv}", "w", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        for node in flattened_nodes:
            writer.writerow(node)

# currently 13 seconds with uv on m2, not bad when running every 5m, mostly waiting on radio
print(f"Runtime: {dt.datetime.now() - ts}")
