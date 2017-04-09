from threads.UdpPingSender import UdpPingSender
from threads.UdpPingResponder import UdpPingResponder
from service.SniffingRegistry import SniffingRegistry

from threading import Thread

from scapy.all import *

registry = SniffingRegistry()
# sender = UdpPingSender("127.0.0.1", 40000, "127.0.0.1", 40001, 1, "measureid")
# responder = UdpPingResponder("127.0.0.1", 40001, "measureid")
sender = UdpPingSender("192.168.0.2", 40000, "192.168.0.15", 40001, 1, "measureid")
responder = UdpPingResponder("192.168.0.2", 40001, "measureid")

sender_thread = Thread(target=sender.run)
responder_thread = Thread(target=responder.run)

sender_thread.start()
responder_thread.start()

sniff(iface="lo", lfilter=registry.is_packet_of_interest, count=1)

# sender_thread.join()
# responder_thread.join()
