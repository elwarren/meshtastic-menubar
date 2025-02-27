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
- Copy `meshtastic-menubar.py` to `$HOME/Library/Application\ Support/xbar/plugins/`
- Edit `$HOME/Library/Application\ Support/xbar/plugins/meshtastic-menubar.py.var.json` to configure options
- Start xbar

# TODO

- Use config file isnstead of xbar variables
- Package for standalone install
- Refactor to use jinja templates

# License 

This project is licensed under the terms of the **GPL-3.0 license**.

