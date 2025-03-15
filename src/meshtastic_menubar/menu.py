import datetime as dt
import os
import meshtastic
from sys import version as python_version

from .util import seconds_to_dhms


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
            f"Version: {self.__version__} | href={self.git_zip_url}", depth=depth + 1
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
    print(self.menu_line(f"xbar (bitbar) | href={self.xbar_repo_url}", depth=depth + 1))
    print(self.menu_line(f"Swiftbar | href={self.swiftbar_repo_url}", depth=depth + 1))
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
        self.menu_line("🟢 Green nodes have been heard in past hour", depth=depth + 1)
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
    uptime_days, uptime_hours, uptime_minutes, uptime_seconds = seconds_to_dhms(uptime)

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
    print(f"--Longitude: {n['position'].get('longitude')} | href='{self.target_url}'")
    print(f"--Altitude: {n['position'].get('altitude')} | href='{self.target_url}'")
    print(f"--Source: {n['position'].get('locationSource')} | href='{self.target_url}'")

    if n["position"].get("time"):
        pos_time = n["position"].get("time")
        # TODO calculate this in get_nodes instead of here in display code
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


def print_menu_nodes(self, nodes):
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
