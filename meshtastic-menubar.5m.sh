#!/bin/bash
#
# Query your Meshtastic device and show discovered nodes in the menubar on macOS and linux.
#
# <xbar.title>Meshtastic Menubar</xbar.title>
# <xbar.version>2025.3.12</xbar.version>
# <xbar.author>elwarren</xbar.author>
# <xbar.author.github>elwarren</xbar.author.github>
# <xbar.desc>Query your Meshtastic device and show discovered nodes in the menubar on macOS and linux.</xbar.desc>
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
#     "meshtastic_menubar"
# ]
# ///


# HACK try to run python if uv isn't installed, probably won't work because package doesn't exist in pypi yet, still sorting how to test that locally
if test -x /opt/homebrew/bin/uv;then
  /opt/homebrew/bin/uv run --no-project --with pytap2 --with meshtastic[cli] --with pyyaml --with requests --python 3.12  -m meshtastic_menubar
else
  python3 -m meshtastic_menubar
fi
