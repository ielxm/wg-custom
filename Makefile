all: install

checkdependencies:
	@echo "Checking if you have all requirements (nmap & wireguard-tools) installed..."
	if [ ! -f /bin/nping ] || [ ! -f /bin/wg ]; \
		then echo "Please ensure that you have all dependencies installed."; exit 1; \
	else echo "--- checkdependencies :: Everything is OK. ---"; fi

install: checkdependencies
	install -m 755 wg-custom /bin/wg-custom
	install -m 755 wg-custom_se /lib/systemd/system-sleep/wg-custom
	install -m 755 wg-custom.service /etc/systemd/system/wg-custom.service
	
	install -Dm600 config_template /etc/wg-custom/config

	systemctl daemon-reload
	
	@echo "Do you want to enable and start wg-custom.service? (y/n)"
	@read answer && if [ $$answer = "y" ]; then systemctl enable --now wg-custom.service; echo "wg-custom.service was successfully enabled and started."; fi

reinstall: checkdependencies
	install -m 755 wg-custom /bin/wg-custom
	install -m 755 wg-custom_se /lib/systemd/system-sleep/wg-custom
	install -m 755 wg-custom.service /etc/systemd/system/wg-custom.service
	
	install -Dm600 config_template /etc/wg-custom/config

	systemctl daemon-reload

	systemctl restart wg-custom

uninstall:
	rm /bin/wg-custom
	rm /lib/systemd/system-sleep/wg-custom
	rm /etc/systemd/system/wg-custom.service

	$(MAKE) uninstallcfg

uninstallcfg:
	@echo "Do you want to remove /etc/wg-custom/config too? (y/n)"
	@read answer && if [ $$answer = "y" ]; then rm -r /etc/wg-custom/; echo "/etc/wg-custom/config was successfully removed."; fi
