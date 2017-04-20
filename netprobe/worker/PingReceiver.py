import select
from scapy.all import *

from packet.MeasurementPacket import MeasurementPacket
from worker.AbstractWorker import AbstractWorker


class PingReceiver(AbstractWorker):
    def __init__(self, self_host, dao):
        super(PingReceiver, self).__init__()
        self.dao = dao

        self.self_host = self_host
        self.self_port = None
        self.proto = ICMP

    def loop_iteration(self):
        time.sleep(3600)
        pass

    def persist_packet(self, packet):
        self.dao.insert(packet[ICMP].id, packet[ICMP].seq, int(packet.time * 1000))
        print "ICMP RCVR: ", packet[ICMP].id, packet[ICMP].seq
        sys.stdout.flush()
