from scapy.all import *

from worker.AbstractWorker import AbstractWorker


class PingSender(AbstractWorker):
    def __init__(self, self_host, target_host, message_interval, measurement_id, dao):
        super(PingSender, self).__init__()
        self.dao = dao
        self.measurement_id = measurement_id
        self.sample_id = 0

        self.self_host = self_host
        self.self_port = None
        self.proto = ICMP

        self.target_host = target_host
        self.message_interval = message_interval


    def loop_iteration(self):
        pkt = IP(dst=self.target_host)/ICMP(id=self.measurement_id, seq=self.sample_id)
        send(pkt, verbose=False)
        self.sample_id = (self.sample_id + 1) % 30000
        time.sleep(self.message_interval)

    def persist_packet(self, packet):
        self.dao.insert(packet[ICMP].id, packet[ICMP].seq, int(packet.time * 1000))
        print "ICMP SNDR: ", packet[ICMP].id, packet[ICMP].seq
        sys.stdout.flush()
