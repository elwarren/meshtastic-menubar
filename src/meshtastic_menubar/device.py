#!/opt/homebrew/bin/uv run --no-project --with pytap2 --with meshtastic[cli] --python 3.12 --script
# -*- coding: utf-8 -*-


import datetime as dt

ts = dt.datetime.now()
import os
import json
from yaml import load
from sys import version as python_version

from .util import recursive_copy, seconds_to_dhms

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
        self.B = B
        self.SHELL = SHELL
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
            self.nodes = recursive_copy(self.iface.nodes)
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
