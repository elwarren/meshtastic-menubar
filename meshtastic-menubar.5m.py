#!/usr/bin/env python3
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
# ]
# ///

import meshtastic_menubar

mm = meshtastic_menubar.MeshtasticMenubar()
mm.cli()
