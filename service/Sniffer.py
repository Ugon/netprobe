from scapy.all import *
from packet.MeasurementPacket import MeasurementPacket


class Sniffer(object):
    def __init__(self, sniffing_registry, interface):
        self.sniffing_registry = sniffing_registry
        self.interface = interface

    def on_packet(self, packet):
        worker = self.sniffing_registry.get_worker_for_packet(packet)
        if worker is not None:
            worker.persist_packet(packet)

    def run(self):
        #lfilter
        sniff(iface=self.interface, prn=self.on_packet)
