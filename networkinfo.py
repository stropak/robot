import os
import re

""" this class is used to find network information """


class NetworkInfo:

    DEFAULT_INTERFACE = "wlan0"

    def __init__(self) -> None:
        pass

    # wifi signal strength
    def get_wifi_signal(self, interface=DEFAULT_INTERFACE):
        signal = os.popen('iwconfig ' + interface +
                          ' | grep "Signal level"').read().strip()
        result = re.findall(r"(-\d+)\s*dBm", signal)
        return int(result[0])

    # IP adress
    def get_ip(self, interface=DEFAULT_INTERFACE):
        ip = os.popen("ip a show " + interface +
                      "| grep inet").read().split("\n")[0].strip()
        ips = re.findall(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", ip)
        return ips[0]
