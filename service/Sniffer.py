from scapy.all import *
from threading import Thread


class Sniffer(object):
    def __init__(self, sniffing_registry, interface):
        self.sniffing_registry = sniffing_registry
        self.interface = interface

        self.thread=None

    def on_packet(self, packet):
        worker = self.sniffing_registry.get_worker_for_packet(packet)
        if worker is not None:
            worker.persist_packet(packet)

    def _run(self):
        # lfilter
        sniff(iface=self.interface, prn=self.on_packet)

    def async_start(self):
        if self.thread is not None:
            raise Exception("cant start what is started")
        else:
            self.thread = Thread(target=self._run)
            self.thread.start()
