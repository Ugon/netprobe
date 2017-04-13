from worker.UdpPingSender import UdpPingSender
from worker.UdpPingResponder import UdpPingResponder
from service.SniffingRegistry import SniffingRegistry
from service.Sniffer import Sniffer

from threading import Thread

from scapy.all import *

registry = SniffingRegistry()
sender = UdpPingSender("127.0.0.2", 40000, "127.0.0.1", 40001, 1, "measureid", None)
responder = UdpPingResponder("127.0.0.2", 40001, "measureid", None)
# sender = UdpPingSender("192.168.0.2", 40000, "192.168.0.15", 40001, 1, "measureid")
# responder = UdpPingResponder("192.168.0.2", 40001, "measureid")

sniffing_registry = SniffingRegistry()
sniffing_registry.register_sender("s", sender)
sniffing_registry.register_responder("r", responder)

sniffer = Sniffer(sniffing_registry, "lo")

sender.async_start()
responder.async_start()

sniffer.async_start()

# time.sleep(20)
#
# sender.stop()



# sender_thread.join()
# responder_thread.join()

1492083077.68
1492083110