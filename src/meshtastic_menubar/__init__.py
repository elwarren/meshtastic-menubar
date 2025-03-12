#!/opt/homebrew/bin/uv run --no-project --with pytap2 --with meshtastic[cli] --python 3.12 --script
# -*- coding: utf-8 -*-


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

__version__ = "2025.3.12"


class MeshtasticMenubar:
    config_file: str
    connection: str
    wifi_host: str
    serial_port: str
    ble_name: str
    use_https: bool
    debug: bool
    log_nodes_jsonl: str
    log_nodes_csv: str
    log_wifi_report: str
    log_traceroute_log: str
    log_dir: str
    bitbar: str
    font_mono: str
    interval: int
    meshtastic_bin: str
    meshtastic_p1: str
    meshtastic_p2: str
    B: str
    SHELL: str

    def __init__(
        self,
        config_file=os.environ.get(
            "MM_CONFIG_FILE",
            os.path.expanduser(f"~/.meshtastic-menubar.yml"),
        ),
        connection="wifi",
        wifi_host="meshtastic.local",
        serial_port="/dev/CU.USBSERIAL-0001",
        ble_name="YOUR_NODE",
        use_https=False,
        debug=False,
        log_nodes_jsonl="meshtastic-menubar-nodes.jsonl",
        log_nodes_csv="meshtastic-menubar-nodes.csv",
        log_wifi_report="meshtastic-menubar-wifi-report.json",
        log_traceroute_log="meshtastic-menubar-traceroute.log",
        log_dir=os.environ.get("HOME"),
        bitbar="xbar",
        font_mono="Menlo-Regular",
        interval=5,
        meshtastic_bin="meshtastic",
        meshtastic_p1="--host",
        meshtastic_p2="meshtastic.local",
        B="|",
        SHELL="shell",
    ):
        """initialize class"""
        self.ts = dt.datetime.now()
        self.config_file = config_file
        self.connection = connection
        self.wifi_host = wifi_host
        self.serial_port = serial_port
        self.ble_name = ble_name
        self.use_https = use_https
        self.debug = debug
        self.log_nodes_jsonl = log_nodes_jsonl
        self.log_nodes_csv = log_nodes_csv
        self.log_wifi_report = log_wifi_report
        self.log_traceroute_log = log_traceroute_log
        self.log_dir = log_dir
        self.bitbar = bitbar
        self.font_mono = font_mono
        self.interval = interval
        self.meshtastic_bin = meshtastic_bin
        self.meshtastic_p1 = meshtastic_p1
        self.meshtastic_p2 = meshtastic_p2
        self.B = (B,)
        self.SHELL = (SHELL,)
        self.git_repo_url = "https://github.com/elwarren/meshtastic-menubar"
        self.git_zip_url = f"{self.git_repo_url}/archive/refs/heads/master.zip"
        self.meshtastic_home_url = "https://meshtastic.org/"
        self.meshtastic_repo_url = "https://github.com/meshtastic/python/"
        self.xbar_repo_url = "https://github.com/matryer/xbar/"
        self.swiftbar_repo_url = "https://github.com/swiftbar/SwiftBar/"
        self.argos_repo_url = "https://github.com/p-e-w/argos"

        if self.config_file:
            if os.path.exists(self.config_file):
                with open(self.config_file, "r") as f:
                    new_config = load(f.read(), Loader=Loader)
                    for param in new_config.keys():
                        setattr(self, param, new_config[param])

        match self.connection:
            case "wifi":
                self.meshtastic_p1 = "--host"
                self.meshtastic_p2 = self.wifi_host

            case "ble":
                self.meshtastic_p1 = "--ble"
                self.meshtastic_p2 = self.ble_name

            case "serial":
                self.meshtastic_p1 = "--port"
                self.meshtastic_p2 = self.serial_port

        # Maybe http saves some battery because https uses more cpu
        if self.use_https:
            self.target_url = f"https://{self.wifi_host}"
        else:
            self.target_url = f"http://{self.wifi_host}"

        self.telemetry_types = self.load_telemetry()
        self.icon = self.load_icons()
        self.txts = self.load_txts()

    def load_icons(self, file: str = None):
        """Load icons from file"""

        # TODO will need to define required icon variable names if we expect to load alternate icons
        return {
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

    def load_telemetry(self, file: str = None):
        """Load telemetry types to send from a yaml file or json"""

        # TODO what are valid telemetry types?
        return [
            "gps",
            "battery",
            "position",
            "user",
            "device",
        ]

    def load_txts(self, file: str = None):
        """Load txt messages to send from a yaml file or json"""
        # TODO move this to optional txt pack that can be loaded without changing code

        return [
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
            # TODO recursive load chicken egg
            # self.icon["wave"],
            # self.icon["thumbsup"],
            # self.icon["thumbsdown"],
            # self.icon["victory"],
            # self.icon["horns"],
            # self.icon["ok_hand"],
            # self.icon["prohibited"],
            # self.icon["one_hundred"],
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

    def recursive_copy(self, obj: dict | list) -> dict:
        """Copy each record to a new `dict` but skip any keys named `raw` because they cannot be sesrialized to JSON"""

        # print(type(obj), obj)
        if isinstance(obj, dict):
            return {k: self.recursive_copy(v) for k, v in obj.items() if k != "raw"}
        elif isinstance(obj, list):
            return [self.recursive_copy(i) for i in obj]
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

    def menu_line(self, line: str, depth: int = 0) -> str:
        """Build a bitbar menu line at variable depths"""
        return "--" * depth + line

    def print_menu_icon(self, menu_status: str = None, menu_icon: str = None):
        """Display icon atop menubar. Optionally accepts a status text to show next to M icon."""

        if menu_icon is None:
            # base64 encoded image of Meshtastic logo
            menu_icon = "iVBORw0KGgoAAAANSUhEUgAAADIAAAAcCAYAAAAjmez3AAAACXBIWXMAAA7DAAAOwwHHb6hkAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAApZJREFUWIXtmE2ITWEYx38zjvFthiFfC5OFaCZFJE2RRCIlysJuFGUxiVkYiylFmWxYTBGbWY2PUhJlwyyFSPmIhOQrYyjEmOHeY3Hcuce5/zPnOfe8d6H86yzuvc/vef7nve857/O+8F8AjAJ2AzUZctQB1W7slK92wAfuA4tTsjXAOSAP9AEr3Vqzqwn4QXAjPjAIHACqjHxniPWBD8BM9zZHlgfcjhjxgTNGfgXwS/CXnDtN0CFh4i1Qb2DHA08EX7haKuBXagkwJAxsNPJdgg1fn4G5bi2XagzwQBQ/beTXEDzcYTb62QeuU+E32TFR9AUw2cDWAi8Fv4PgrRf9fo9j78NqBnKRYjlgtZHvptTsxT+/qek6ADS6sV7UBOCpMHLcyG8SbB8wIxRzUMTcAUZndh/SKVHkMTDOwE4D3gl+ayTOA26JuI7s9gOtpfSB/AksN/LnhbnumNiFwHdRa1l51ouqA14JI4eN/HbBvgamjMC0CeYRMDa9/aJ6RNJ72JrE2cDHCJsH1idw1UCvqHs0vf1Am0WyQWCRkb8i+C4j2wB8ibA5YJWRH9Z04L0w0m7kdwn2GTAxhYedIsdzYFKKHFwQSW4Q7D+S1IAezXLa9MvCx0kr3CLgb8B8Axs3vzvt3v/SLKA/kisPbEgC5wCfhJFWY+F9gn1ItjfOFpHzDTA1DqgCrgroGrbN0gL0GrC03DsI6azw1RMX3CqCrS21B9wUvKtVOW492xYNnAd8FYHWTU6HYF33Seso7TD6iWyPTwgj1m1nPaWDMEDQbriW6vmOhAM8YD/Fw4S0BwGNBP9AIfnezJa1wl34EEHHLJeEJuAuYu4ZVBiM3rjkjtRM0CYlHj95GQtV8iYKsh45/Xv6DTfbUnnkjAuSAAAAAElFTkSuQmCC"

        if menu_status:
            print(f"{menu_status} | templateImage='{menu_icon}'")
        else:
            print(f" | templateImage='{menu_icon}'")

        print("---")

    def print_menu_bar(self, depth: int = 0):
        """Display Meshtastic Menubar submenu"""
        print(self.menu_line(f"Meshtastic Menubar", depth))

    def print_menu_about(self, depth: int = 1):
        """Display About submenu"""
        print(self.menu_line(f"{self.icon['waffle']} About", depth))
        print(
            self.menu_line(
                f"Meshtastic Menubar | href={self.git_repo_url}", depth=depth + 1
            )
        )
        print(
            self.menu_line(
                f"Version: {VERSION} | href={self.git_zip_url}", depth=depth + 1
            )
        )

        print(self.menu_line("---", depth=depth + 1))

        print(self.menu_line("Built with:", depth=depth + 1))
        print(
            self.menu_line(
                f"Meshtastic Project | href={self.meshtastic_home_url}", depth=depth + 1
            )
        )
        print(
            self.menu_line(
                f"Meshtastic Python | href={self.meshtastic_repo_url}", depth=depth + 1
            )
        )
        print(
            self.menu_line(
                f"xbar (bitbar) | href={self.xbar_repo_url}", depth=depth + 1
            )
        )
        print(
            self.menu_line(f"Swiftbar | href={self.swiftbar_repo_url}", depth=depth + 1)
        )
        print(self.menu_line(f"Argos | href={self.argos_repo_url}", depth=depth + 1))

    def print_menu_refresh(self, depth: int = 1):
        """Display Refresh submenu"""
        print(self.menu_line("---", depth))
        print(self.menu_line(f"{self.icon['refresh']} Refresh | refresh=true", depth))

    def print_menu_broadcast(self, depth: int = 1):
        """Display node Broadcast submenu"""
        print(self.menu_line(f"{self.icon['satellite']} Broadcast", depth))

        for txt in self.txts:
            # TODO new machine has different setup than my build machine. zsh: command not found: meshtastic
            # TODO i hate shell escaping in these apps
            # "meshtastic.local" 'meshtastic' --port /dev/cu.usbserial-0001 --sendtext What up?
            # zsh: no matches found: up?
            print(
                self.menu_line(
                    f"{txt} | {self.SHELL}='meshtastic' {self.B} terminal=true {self.B} param1={self.meshtastic_p1} {self.B} param2={self.meshtastic_p2} {self.B} param3='--sendtext' {self.B} param4='{txt}'",
                    depth=depth + 1,
                )
            )

    def print_menu_device(self, depth: int = 1):
        """Display host Device submenu"""

        print(self.menu_line(f"{self.icon['gear']} Device", depth))
        print(
            self.menu_line(
                f"Reboot | {self.SHELL}='meshtastic' {self.B} terminal=true {self.B} param1={self.meshtastic_p1} {self.B} param2={self.meshtastic_p2} {self.B}param3='--reboot'",
                depth=depth + 1,
            )
        )
        print(
            self.menu_line(
                f"Shutdown | {self.SHELL}='meshtastic' {self.B} terminal=true {self.B} param1={self.meshtastic_p1} {self.B} param2={self.meshtastic_p2} {self.B}param3='--shutdown'",
                depth=depth + 1,
            )
        )
        print(
            self.menu_line(
                f"Tail logs | {self.SHELL}='meshtastic' {self.B} terminal=true {self.B} param1={self.meshtastic_p1} {self.B} param2={self.meshtastic_p2} {self.B}param3='--noproto'",
                depth=depth + 1,
            )
        )
        print(
            self.menu_line(
                f"BLE Scan | {self.SHELL}='meshtastic' {self.B} terminal=true {self.B} param1={self.meshtastic_p1} {self.B} param2={self.meshtastic_p2} {self.B}param3='--ble-scan'",
                depth=depth + 1,
            )
        )
        print(
            self.menu_line(
                f"json Report | {self.SHELL}='open' {self.B} terminal=false {self.B} param1='{self.target_url}/json/report'",
                depth=depth + 1,
            )
        )

    def print_menu_debug(self, depth: int = 1):
        """Build and display Debug submenu"""

        print(self.menu_line(f"{self.icon['exclaim']} Debug", depth))

    def print_menu_environment(self, depth: int = 1):
        """Build and display Debug Nodelist submenu"""

        print(self.menu_line("Environment", depth=depth))
        for var in sorted(os.environ):
            print(self.menu_line(f"{var}={os.environ[var]}", depth=depth + 1))

    def print_menu_nodelist(self, nodelist: str, depth: int = 1):
        """Build and display Debug Nodelist submenu"""

        print(self.menu_line("Node List", depth=depth))
        for nodelist_node in nodelist:
            print(self.menu_line(f"Node: {nodelist_node}", depth=depth + 1))

    def print_menu_config(self, depth: int = 1):
        """Build and display Configuration submenu"""

        print(self.menu_line(f"Config", depth=depth))
        print(
            self.menu_line(
                f"Edit Config File: {self.config_file} | shell='vi' | terminal=true | param1={self.config_file}",
                depth=depth + 1,
            )
        )

        for param in vars(self).items():
            # print(self.menu_line(f"{param}={self[param]}", depth=depth + 1))
            print(self.menu_line(f"{param}", depth=depth + 1))

    def print_menu_versions(self, depth: int = 1):
        """Show package versions submenu"""

        print(self.menu_line("Versions", depth))
        print(self.menu_line(f"Python: {python_version}", depth=depth + 1))
        print(
            self.menu_line(
                f"Meshtastic: {meshtastic.version.get_active_version()}",
                depth=depth + 1,
            )
        )

    def print_menu_help(self, depth: int = 1):
        """Show Help submenu"""

        print(self.menu_line("---", depth))
        print(self.menu_line(f"{self.icon['question']} Help", depth))

        print(
            self.menu_line(
                "🟢 Green nodes have been heard in past hour", depth=depth + 1
            )
        )
        print(self.menu_line("🟡 Yellow nodes three hours", depth=depth + 1))
        print(self.menu_line("🟠 Orange 12 hours", depth=depth + 1))
        print(self.menu_line("🔴 Red past three days", depth=depth + 1))
        print(self.menu_line("🟣 Purple heard in past seven days", depth=depth + 1))
        print(
            self.menu_line(
                "🔵 Blue nodes are ice cold, we haven't heard from them in over a week",
                depth=depth + 1,
            )
        )
        print(
            self.menu_line(
                "⚫ Black nodes were partially received without timestamp",
                depth=depth + 1,
            )
        )
        print(self.menu_line("---", depth=depth + 1))
        print(self.menu_line(f"📚 RTFM | href='{self.git_repo_url}'", depth=depth + 1))

    def print_menu_node_heard(
        self,
        n,
        status_icon,
        heard_str,
        heard_ago,
        heard_ago_total_seconds,
        heard_at_dt,
        heard_last,
    ):
        """Display node Heard submenu"""
        print(f"--{self.icon['satdish']} Heard")
        print(f"--SNR: {n.get('snr')} | href='{self.target_url}'")
        print(f"--Hops away: {n.get('hopsAway')} | href='{self.target_url}'")
        print(f"--Last: {heard_str}| href='{self.target_url}'")
        print(f"--Seconds: {heard_ago_total_seconds}| href='{self.target_url}'")
        print(f"--DT: {heard_at_dt}| href='{self.target_url}'")
        # print(f"--Epoc: {heard_last}| href='{self.target_url}'")

    def print_menu_node_device(self, n):
        """Display node Device submenu"""
        uptime = int(n["deviceMetrics"].get("uptimeSeconds", 0))
        uptime_days, uptime_hours, uptime_minutes, uptime_seconds = (
            MeshtasticMenubar.seconds_to_dhms(uptime)
        )

        print("-----")
        print(f"--{self.icon['pager']} Device")

        print(
            f"--Battery: {n['deviceMetrics'].get('batteryLevel', None)}% | href='{self.target_url}'"
        )

        print(
            f"--Voltage: {n['deviceMetrics'].get('voltage', None)} | href='{self.target_url}'"
        )
        print(
            f"--Channel Util: {n['deviceMetrics'].get('channelUtilization')} | href='{self.target_url}'"
        )
        print(
            f"--Air Util: {n['deviceMetrics'].get('airUtilization')} | href='{self.target_url}'"
        )
        print(
            f"--Uptime: {uptime_days}d {uptime_hours}h {uptime_minutes}m {uptime_seconds}s| href='{self.target_url}'"
        )
        print(f"--Seconds: {uptime}| href='{self.target_url}'")

    def print_menu_node_user(self, n):
        """Display node User submenu"""
        print("-----")
        print(f"--{self.icon['ticket']} User")
        print(f"--Name: {n['user'].get('longName')} | href='{self.target_url}'")
        print(f"--Short: {n['user'].get('shortName')} | href='{self.target_url}'")
        print(f"--Model: {n['user'].get('hwModel')} | href='{self.target_url}'")
        print(f"--Role: {n['user'].get('role')} | href='{self.target_url}'")
        print(f"--PK: {n['user'].get('publicKey')} | href='{self.target_url}'")

    def print_menu_node_position(self, n):
        """Display node Position submenu"""

        print("-----")
        print(f"--{self.icon['globe_america']} Position")
        # TODO copy latlon to buffer for copypasta when clicked
        print(f"--Latitude: {n['position'].get('latitude')} | href='{self.target_url}'")
        print(
            f"--Longitude: {n['position'].get('longitude')} | href='{self.target_url}'"
        )
        print(f"--Altitude: {n['position'].get('altitude')} | href='{self.target_url}'")
        print(
            f"--Source: {n['position'].get('locationSource')} | href='{self.target_url}'"
        )

        if n["position"].get("time"):
            pos_time = n["position"].get("time")
            print(
                f"--Time: {dt.datetime.fromtimestamp(pos_time)} | href='{self.target_url}'"
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

    def print_menu_node_comms(self, node):
        """Display node Comms submenu"""

        print("-----")
        print(f"--{self.icon['satellite']} Comms")

        # HACK the node id starts with ! which is being interpreted by the shell, need to escape them, vscode is eating this on save somehow https://github.com/swiftbar/SwiftBar/issues/308
        if self.bitbar == "xbar":
            node_escaped = node.replace("!", r"\!")
        if self.bitbar == "swiftbar":
            node_escaped = node
        if self.bitbar == "argos":
            # TODO unknown shell escape behavior in argos
            node_escaped = node
        if self.bitbar == "local":
            node_escaped = node.replace("!", r"\!")

        print(
            f"--Traceroute | {self.SHELL}='meshtastic' {self.B} terminal=true {self.B} param1={self.meshtastic_p1} {self.B} param2={self.meshtastic_p2} {self.B} param3='--traceroute' {self.B} param4='{node_escaped}' {self.B} param5='|' {self.B} param6='tee {self.log_dir}/{self.log_traceroute_log}'"
        )

        print("--Request")
        print(
            f"----Request position | {self.SHELL}='meshtastic' {self.B} terminal=true {self.B} param1={self.meshtastic_p1} {self.B} param2={self.meshtastic_p2} {self.B} param3='--request-position' {self.B} param4='--dest' {self.B} param5='{node_escaped}'"
        )

        print("----Telemetry")
        for telemetry_type in self.telemetry_types:
            print(
                f"----{telemetry_type} | {self.SHELL}='meshtastic' {self.B} terminal=true {self.B} param1={self.meshtastic_p1} {self.B} param2={self.meshtastic_p2} {self.B} param3='--request-telemetry' {self.B} param4='{telemetry_type}' {self.B} param5='--dest' {self.B} param6='{node_escaped}' "
            )

        print(f"--Send text")
        for txt in self.txts:
            print(
                f"----{txt} | terminal=true {self.B} {self.SHELL}='meshtastic' {self.B} param1={self.meshtastic_p1} {self.B} param2={self.meshtastic_p2} {self.B} param3='--sendtext' {self.B} param4='{txt}' {self.B} param5='--dest' {self.B} param6='{node_escaped}'"
            )

    def get_node_short_name(self, n):
        # have to reach into potentially missing keys to build main menu
        try:
            return n["user"].get("shortName")
        except:
            return None

    def get_node_hops_icon(self, n):
        """Return an emoji based on hopsAway"""

        match n.get("hopsAway"):
            case 0:
                return self.icon["zero"]
            case 1:
                return self.icon["one"]
            case 2:
                return self.icon["two"]
            case 3:
                return self.icon["three"]
            case 4:
                return self.icon["four"]
            case 5:
                return self.icon["five"]
            case 6:
                return self.icon["six"]
            case 7:
                return self.icon["seven"]
            case 8:
                return self.icon["eight"]
            case 9:
                return self.icon["nine"]
            case _:
                return self.icon["star"]

    def calculate_heards(self, heard_last=None):
        # if heard_last is None then black because we can't calculate time without it
        status_icon = self.icon["black"]
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
            heard_days, heard_hours, heard_minutes, heard_seconds = (
                MeshtasticMenubar.seconds_to_dhms(heard_ago_total_seconds)
            )

            if self.debug:
                print(
                    f"heard_ago {heard_ago} = now {ts} - heard_at_dt {heard_at_dt} heard_ago_seconds {heard_ago_total_seconds}"
                )

            # blue is on ice because it's been over a week since we heard from them
            status_icon = self.icon["blue"]

            # purple if heard in last week
            if heard_days < 8:
                status_icon = self.icon["purple"]

            # red if heard in last 3 days
            if heard_days < 4:
                status_icon = self.icon["red"]

            # orange if heard in last 12 hours 43200 sec
            if heard_ago_total_seconds < (12 * 60 * 60):
                status_icon = self.icon["orange"]

            # yellow if heard in last three hours 10800 sec
            if heard_ago_total_seconds < (3 * 60 * 60):
                status_icon = self.icon["yellow"]

            # green if heard in last hour 3600 sec
            if heard_ago_total_seconds < (1 * 60 * 60):
                status_icon = self.icon["green"]

            heard_str = (
                f"{heard_days}d {heard_hours}h {heard_minutes}m {heard_seconds}s"
            )

        return (
            status_icon,
            heard_str,
            heard_ago,
            heard_ago_total_seconds,
            heard_at_dt,
            heard_last,
        )

    def print_menu_nodes(self, nodes):
        """Display all Nodes and their submenus"""

        # NOTE default lastHeard to zero because relayed nodes do not report and we need this to sort
        nodelist = sorted(
            nodes, reverse=True, key=lambda x: nodes[x].get("lastHeard", 0)
        )
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
            ) = self.calculate_heards(heard_last=node.get("lastHeard"))

            #
            # First line is always our node so it gets a special mesh icon
            #
            if first_node:
                first_node = False
                print(
                    f"{self.icon['globe_mesh']} {id} {self.icon['hash']} {self.get_node_short_name(node)} | font={self.font_mono}"
                )
            else:
                print(
                    f"{status_icon} {id} {self.get_node_hops_icon(node)} {self.get_node_short_name(node)} | font={self.font_mono}"
                )

            #
            # First submenu
            #
            # Heard submenu
            #
            self.print_menu_node_heard(
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
                self.print_menu_node_user(node)

            #
            # Metrics menu
            #
            if node.get("deviceMetrics"):
                self.print_menu_node_device(node)

            #
            # Position menu
            #
            if node.get("position"):
                self.print_menu_node_position(node)

            #
            # Comms menu
            #
            self.print_menu_node_comms(id)

    def get_iface(self, connection: str = "wifi"):
        """Initialize meshtastic and return iface object"""

        if connection == "wifi":
            # TODO is importing late bad style? Trying to reduce imports and speed startup
            try:
                import meshtastic.tcp_interface

                hostname = self.wifi_host
                self.iface = meshtastic.tcp_interface.TCPInterface(hostname=hostname)
            except Exception as e:
                print(f"Exception connecting host: {self.wifi_host} via Wifi: {e}")
                no_device = str(e)
                # TODO could be wrong or missing hostname but sometimes wifi just doesn't respond. Not sure is mdns, maybe try IP next time
                # Exception connecting via Wifi: [Errno 8] nodename nor servname provided, or not known
                # [Errno 8] nodename nor servname provided, or not known

        elif connection == "ble":
            try:
                import meshtastic.ble_interface

                self.iface = meshtastic.ble_interface.BLEInterface(
                    address=self.ble_name
                )
            except Exception as e:
                print(f"Exception connecting via Bluetooth: {e}")
                no_device = str(e)

        elif connection == "serial":
            # fail fast if device doesn't exist or path incorrect
            serial_fail = False
            if self.serial_port:
                if os.path.exists(self.serial_port):

                    try:
                        import meshtastic.serial_interface

                        self.iface = meshtastic.serial_interface.SerialInterface(
                            self.serial_port
                        )
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
                self.print(f"Serial device does not exist at: {self.serial_port}")
                no_device = "No connection method set"
                self.print_menu_debug(depth=0)
                self.print_menu_environment(depth=1)
                self.print_menu_config(depth=1)
                # should we exit 0 or 1? how does xbar handle this vs swiftbar?
                exit(0)

        return self

    def get_nodes(self) -> dict:
        """Get nodes from existing meshtastic connection iface"""

        try:
            self.nodes = self.recursive_copy(self.iface.nodes)
        except Exception as e:
            print(f"Exception getting nodes via Wifi: {e}")

        return self.nodes

    def save_wifi_report(self):
        """Download /json/report from a wifi connected meshtastic device"""

        if self.log_wifi_report and self.connection == "wifi":
            import requests

            with open(
                f"{self.log_dir}/{self.log_wifi_report}",
                "a",
                encoding="utf-8",
            ) as f:
                f.write(
                    json.dumps(
                        {
                            "timestamp": str(ts),
                            "report": requests.get(
                                f"{self.target_url}/json/report", timeout=10
                            ).json(),
                        }
                    )
                    + "\n"
                )

    def save_nodes_csv(self) -> None:
        """Write nodes to a CSV file."""

        if not self.log_nodes_csv:
            return None

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

        flattened_nodes = [flatten_node(node) for node in self.nodes.values()]

        # sort unique keys for header so git diff is consistent
        keys = set()
        for node in flattened_nodes:
            keys.update(node.keys())
        keys = sorted(list(keys))

        with open(
            f"{self.log_dir}/{self.log_nodes_csv}",
            "w",
            encoding="utf-8",
        ) as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=keys)
            writer.writeheader()
            for node in flattened_nodes:
                writer.writerow(node)

    def save_nodes_jsonl(self) -> None:
        """Append nodes to line delimited json."""
        if not self.log_nodes_jsonl:
            return None

        with open(
            f"{self.log_dir}/{self.log_nodes_jsonl}",
            "a",
            encoding="utf-8",
        ) as f:
            # HACK skipkeys is fix for Position not serializable only on serial not wifi
            f.write(
                # json.dumps({"timestamp": str(ts), "nodes": nodes}, skipkeys=True) + "\n"
                json.dumps({"timestamp": str(ts), "nodes": self.nodes})
                + "\n"
            )

    def cli(self):
        """This is __main__ code when called as cli vs testing."""

        #
        # show menu bar icon asap so that if we throw exception we still have a menu
        #
        self.print_menu_icon()

        self.no_device = False
        self.test_empty = False

        #
        # get meshtastic interface depending on connection type
        #
        # self.iface = self.get_iface()
        iface = self.get_iface()

        if self.iface is None:
            print("No connection method set")
            print("Choose wifi, ble, or serial")
            self.no_device = "No connection method set"
            self.print_menu_debug(depth=0)
            self.print_menu_environment(depth=1)
            self.print_menu_config(depth=1)
            # should we exit 0 or 1? how does xbar handle this vs swiftbar?
            exit(0)

        nodes = self.get_nodes()

        if self.debug:
            print("Environment:\n", json.dumps(dict(os.environ)))
            print("Nodes:\n", json.dumps(self.nodes))
            exit(0)

        #
        # main menu display output
        #
        self.print_menu_bar(depth=0)

        #
        # menu drop down begin
        #
        self.print_menu_about(depth=1)
        self.print_menu_refresh(depth=1)
        self.print_menu_broadcast(depth=1)
        self.print_menu_device(depth=1)

        self.print_menu_debug(depth=1)
        self.print_menu_environment(depth=2)
        self.print_menu_config(depth=2)
        self.print_menu_versions(depth=2)

        self.print_menu_help(depth=1)

        #
        # back to main menu again
        #
        print(f"Every: {self.interval}m Last Run:")
        print(f"{self.ts.replace(microsecond=0)}")
        print("---")

        # bail out if no nodes nothing to show
        if self.test_empty or self.no_device or len(self.nodes) < 1:
            print(f"{self.icon['police']} No Device or Nodes!")
            # show no_device holds our exception text
            print(self.no_device)
            exit(0)

        self.print_menu_nodes(self.nodes)
        #
        # End nodes submenu
        #

        #
        # Final act
        #
        self.save_wifi_report()
        self.save_nodes_csv()
        self.save_nodes_jsonl()

        self.iface.close
        # currently 13 seconds with uv on m2, not bad when running every 5m, mostly waiting on radio
        print(f"Runtime: {dt.datetime.now() - self.ts}")
