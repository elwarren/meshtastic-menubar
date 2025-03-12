#!/usr/bin/env pytest

import pytest
import sys

import meshtastic_menubar


class TestMeshtasticMenubar:

    def test_seconds(self):
        assert meshtastic_menubar.MeshtasticMenubar.seconds_to_dhms(86400)

    def test_load_telemetry(self):
        mm = meshtastic_menubar.MeshtasticMenubar()
        assert mm.load_telemetry() is not None


if __name__ == "__main__":
    sys.exit(pytest.main(["-vv"]))
