# Custom WireGuard scripts & service

``wg-custom`` bypasses (it used to bypass) the WireGuard protocol block by modifying (blurring, adding extra random bytes) before the protocol handshake + provides a systemd-service file, a hook for connecting/disconnecting ``wg-custom`` after/before hibernation, and a config converter (WireGuard -> ``wg-custom``).
