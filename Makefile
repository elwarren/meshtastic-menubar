
help:
	@grep -E '^\w' Makefile

clean:
	rm $$HOME/.meshtastic-menubar.json && true
	rm $$HOME/.meshtastic-menubar.log && true
	rm $$HOME/.meshtastic-menubar.csv && true
	
deps:
	brew install uv
	brew install xbar

install_xbar:
	cp meshtastic-menubar.py $$HOME/Library/Application\ Support/xbar/plugins/meshtastic-menubar.5m.py

install_swiftbar:
	cp meshtastic-menubar.py $$HOME/Library/Application\ Support/SwiftBar/Plugins/meshtastic-menubar.5m.py

install_config:
	cp config.yml $$HOME/.meshtastic-menubar.yml

install: deps check install_xbar install_config

uninstall:
	rm $$HOME/Library/Application\ Support/xbar/plugins/meshtastic-menubar.5m.py && true
	rm $$HOME/Library/Application\ Support/SwiftBar/Plugins/meshtastic-menubar.5m.py && true

check:
	@date
	@echo "Checking for brew"
	brew --version && true
	@echo "Checking for uv"
	uv --version && true

	@echo "Checking for xbar"
	test -f /Applications/xbar.app/Contents/MacOS/xbar && true
	@echo "Checking for SwiftBar"
	test -f /Applications/SwiftBar.app/Contents/MacOS/SwiftBar && true

	# TODO uv will handle this but keeping for debugging purposes
	@echo "Checking for Python 3"
	python3 --version && true
	@echo "Checking for pip3"
	pip3 --version && true

run:
	open -a xbar
	