# meshtastic-menubar

Query your Meshtastic device and show discovered nodes.

# Features

Lists nodes in order of last heard with most recent at top.

- 🟢 Green nodes have been heard in past hour
- 🟡 Yellow nodes three hours
- 🟠 Orange 12 hours
- 🔴 Red past three days
- 🟣 Purple heard in past seven days
- 🔵 Blue nodes are ice cold, we haven't heard from them in over a week
- ⚫ Black nodes were partially received without timestamp

# Setup

Requires a meshtastic device already configured to work with meshtastic-cli before using this app.

## Automatic

- Run `make install` in terminal on macos.

## Manual

- Install uv
- uv will install python 3.12 on first run
- Install xbar
- Copy `meshtastic-menubar.5m.py` to `$HOME/Library/Application\ Support/xbar/plugins/`
- Edit `$HOME/Library/Application\ Support/xbar/plugins/meshtastic-menubar.5m.py.var.json` to configure options
- Start xbar

# Config file

Will read parameters from config file in yaml format.

- Choices for `bitbar` are `xbar`, `swiftbar`, or `argos`
- Choices for `connection` are `wifi`, `bluetooth`, or `serial`


```
bitbar: xbar
connection: serial
serial_port: /dev/cu.usbserial-0001
debug: False
use_https: False
wifi_host: meshtastic.local
log_nodes_jsonl: meshtastic-menubar-nodes.jsonl
log_nodes_csv: meshtastic-menubar-nodes.csv
log_wifi_report: meshtastic-menubar-wifi-report.json
log_traceroute_log: meshtastic-menubar-traceroute.log
log_dir: /tmp
font_mono: Menlo-Regular
interval: 5
```

# License

This project is licensed under the terms of the **GPL-3.0 license**.

