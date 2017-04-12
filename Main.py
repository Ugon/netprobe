from worker.UdpPingSender import UdpPingSender
from worker.UdpPingResponder import UdpPingResponder
from service.SniffingRegistry import SniffingRegistry
from service.MeasurementService import MeasurementService
from service.Sniffer import Sniffer

from threading import Thread

from scapy.all import *

sniffing_registry = SniffingRegistry()
service = MeasurementService("127.0.0.1", sniffing_registry)

sniffer = Sniffer(sniffing_registry, "lo")
sniffer_thread = Thread(target=sniffer.run)
sniffer_thread.start()


service.start_udp_sender(40000, "127.0.0.2", 40001, 1, "measureid")
service.start_udp_responder(40001, "measureid")

time.sleep(10)

service.stop_udp_sender("measureid")
service.stop_udp_responder("measureid")

# sender = UdpPingSender("127.0.0.1", 40000, "127.0.0.2", 40001, 1, "measureid")
# responder = UdpPingResponder("127.0.0.1", 40001, "measureid")
# sender = UdpPingSender("192.168.0.2", 40000, "192.168.0.15", 40001, 1, "measureid")
# responder = UdpPingResponder("192.168.0.2", 40001, "measureid")

# sniffing_registry = SniffingRegistry()
# sniffing_registry.register_sender("s", sender)
# sniffing_registry.register_responder("r", responder)
#
sniffer = Sniffer(sniffing_registry, "lo")
#
# sender.async_start()
# responder.async_start()
# sniffer_thread = Thread(target=sniffer.run)
#
# sniffer_thread.start()

# time.sleep(10)
#
# sender.stop()




# sender_thread.join()
# responder_thread.join()
