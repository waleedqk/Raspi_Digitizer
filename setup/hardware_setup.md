
# Netgear DGN3500 Router

**Product Page**
https://www.netgear.com/support/product/DGN3500.aspx

## OpenWRT

The router runs the OpenWRT. OpenWrt Project is a Linux operating system targeting embedded devices.

**ProjectPage**
https://openwrt.org/

## Firmware Update

1) To update the firmware on the router, search through the Hardware Table and find the correct hardware: Netgear DGN3500

    https://openwrt.org/toh/views/toh_fwdownload?dataflt%5BBrand*~%5D=NETGEAR&dataflt%5BModel*~%5D=DGN3500

2) Since we want to do a firmware upgrade - Download the ```Firmware OpenWrt Upgrade URL``` ".bin" file that is associated with the hardware.



## Upgrade The Web Portal - LuCI

https://openwrt.org/docs/guide-user/luci/luci.essentials
https://oldwiki.archive.openwrt.org/doc/howto/luci.essentials

### Online Installation

SSH into the router:

    ssh root@192.168.1.1

    opkg update && opkg install luci
    opkg install luci-ssl # enable https for luci

### Offline Installation

scp luci_0.11.1-1_ar71xx.ipk luci-app-firewall_0.11.1-1_ar71xx.ipk luci-i18n-english_0.11.1-1_ar71xx.ipk luci-lib-core_0.11.1-1_ar71xx.ipk luci-lib-ipkg_0.11.1-1_ar71xx.ipk luci-lib-nixio_0.11.1-1_ar71xx.ipk luci-lib-sys_0.11.1-1_ar71xx.ipk luci-lib-web_0.11.1-1_ar71xx.ipk luci-mod-admin-core_0.11.1-1_ar71xx.ipk luci-mod-admin-full_0.11.1-1_ar71xx.ipk luci-proto-core_0.11.1-1_ar71xx.ipk luci-proto-ppp_0.11.1-1_ar71xx.ipk luci-sgi-cgi_0.11.1-1_ar71xx.ipk luci-theme-base_0.11.1-1_ar71xx.ipk luci-theme-openwrt_0.11.1-1_ar71xx.ipk root@192.168.1.1:\root

Install the packages in the order:

opkg install luci-proto-core_0.11.1-1_ar71xx.ipk
opkg install luci-lib-core_0.11.1-1_ar71xx.ipk
opkg install luci-lib-sys_0.11.1-1_ar71xx.ipk
opkg install luci-lib-nixio_0.11.1-1_ar71xx.ipk
opkg install luci-sgi-cgi_0.11.1-1_ar71xx.ipk
opkg install luci-lib-web_0.11.1-1_ar71xx.ipk
opkg install luci-i18n-english_0.11.1-1_ar71xx.ipk
opkg install luci-mod-admin-core_0.11.1-1_ar71xx.ipk
opkg install luci-lib-ipkg_0.11.1-1_ar71xx.ipk
opkg install luci-mod-admin-full_0.11.1-1_ar71xx.ipk
opkg install luci-theme-base_0.11.1-1_ar71xx.ipk
opkg install luci-theme-openwrt_0.11.1-1_ar71xx.ipk
opkg install luci-app-firewall_0.11.1-1_ar71xx.ipk
opkg install luci-proto-ppp_0.11.1-1_ar71xx.ipk
opkg install luci_0.11.1-1_ar71xx.ipk

**Start and Enable the web server (uHTTPd)**

The web server software uHTTPd is a dependency of the LuCI package and is automatically installed when you install LuCI. After installation the web server is not running! You need to manually start the web server. You should also enable the web server, so that it automatically starts up whenever you reboot the router. The first command below starts the web server, the second enables it across reboots.

    /etc/init.d/uhttpd start
    /etc/init.d/uhttpd enable

## Upgrading OpenWrt firmware from the Command Line

https://openwrt.org/docs/guide-user/installation/sysupgrade.cli