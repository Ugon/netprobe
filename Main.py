from threads.UdpPingSender import UdpPingSender
from threads.UdpPingResponder import UdpPingResponder
from service.SniffingRegistry import SniffingRegistry
from service.Sniffer import Sniffer

from threading import Thread

from scapy.all import *

registry = SniffingRegistry()
# sender = UdpPingSender("127.0.0.1", 40000, "127.0.0.1", 40001, 1, "measureid")
# responder = UdpPingResponder("127.0.0.1", 40001, "measureid")
sender = UdpPingSender("192.168.0.2", 40000, "192.168.0.15", 40001, 1, "measureid")
responder = UdpPingResponder("192.168.0.2", 40001, "measureid")

sniffing_registry = SniffingRegistry()
sniffing_registry.register_sender("s", sender)
sniffing_registry.register_responder("r", responder)

sniffer = Sniffer(sniffing_registry)

sender_thread = Thread(target=sender.run)
responder_thread = Thread(target=responder.run)
sniffer_thread = Thread(target=sniffer.run)

sender_thread.start()
responder_thread.start()
sniffer_thread.start()




# sender_thread.join()
# responder_thread.join()
