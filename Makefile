
help:
	@grep -E '^\w' Makefile

clean:
	rm $$HOME/.meshtastic-menubar.json || true
	rm $$HOME/.meshtastic-menubar.log || true
	rm $$HOME/.meshtastic-menubar.csv || true
	
deps:
	HOMEBREW_NO_AUTO_UPDATE=1 brew install uv
	HOMEBREW_NO_AUTO_UPDATE=1 brew install xbar

install_xbar:
	cp meshtastic-menubar.py $$HOME/Library/Application\ Support/xbar/plugins/meshtastic-menubar.5m.py

install_swiftbar:
	cp meshtastic-menubar.py $$HOME/Library/Application\ Support/SwiftBar/Plugins/meshtastic-menubar.5m.py

install_config:
	cp config.yml $$HOME/.meshtastic-menubar.yml

install: deps check install_xbar install_config

uninstall: uninstall_xbar

uninstall_xbar:
	rm $$HOME/Library/Application\ Support/xbar/plugins/meshtastic-menubar.5m.py || true

uninstall_swiftbar:
	rm $$HOME/Library/Application\ Support/SwiftBar/Plugins/meshtastic-menubar.5m.py || true

check: check_macos

check_macos:
	# 
	# Checking dependencies to help debugging 
	@date
	#
	@echo "Checking for brew"
	HOMEBREW_NO_AUTO_UPDATE=1 brew --version || true
	#
	@echo "Checking for xbar"
	test -f /Applications/xbar.app/Contents/MacOS/xbar && echo "Found xbar" || echo "Cannot find xbar"
	#
	@echo "Checking for SwiftBar"
	test -f /Applications/SwiftBar.app/Contents/MacOS/SwiftBar && echo "Found SwiftBar" || echo "Cannot find SwiftBar"
	# 
	@echo "Checking for uv"
	uv --version || true
	# 
	# TODO uv will handle this but keeping for debugging purposes
	@echo "Checking for Python 3"
	python3 --version || true
	#
	@echo "Checking for pip3"
	pip3 --version || true
	# 
	@echo Check local version of meshtastic-menubar.py here
	grep -E '^VERSION' meshtastic-menubar.py
	#
	@echo Check xbar version of meshtastic-menubar.py in xbar
	grep -E '^VERSION' $$HOME/Library/Application\ Support/xbar/plugins/meshtastic-menubar.5m.py
	#
	@echo Check config file for meshtastic-menubar.py in HOME
	test -f $$HOME/.meshtastic-menubar.yml && echo "Found config in $$HOME" || echo "Cannot find config in $$HOME"
	#

run:
	open -a xbar
