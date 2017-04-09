from scapy.all import *
from packet.MeasurementPacket import MeasurementPacket


class Sniffer(object):
    def __init__(self, sniffing_registry):
        self.sniffing_registry = sniffing_registry

    def on_packet(self, packet):
        worker = self.sniffing_registry.get_worker_for_packet(packet)
        if worker is not None:
            worker.persist(packet)

    def run(self):
        #lfilter
        sniff(iface="wlan0", prn=self.on_packet)
