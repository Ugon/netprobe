from scapy.all import *

from packet.MeasurementPacket import MeasurementPacket
from worker.AbstractWorker import AbstractWorker
import sys


class UdpPingReceiver(AbstractWorker):
    def __init__(self, self_host, self_port, sock, measurement_id, dao):
        super(UdpPingReceiver, self).__init__()
        self.dao = dao
        self.measurement_id = measurement_id

        self.self_host = self_host
        self.self_port = self_port
        self.proto = UDP

        self.socket = sock
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def loop_iteration(self):
        ready = select([self.socket], [], [], 1)
        if ready[0]:
            self.socket.recv(64 * 1024)

    def persist_packet(self, packet):
        measurement_packet = MeasurementPacket.from_binary(packet[UDP].payload.load)
        self.dao.insert(measurement_packet.measurement_id, measurement_packet.sample_id, int(packet.time * 1000))
        print "RECEIVER:  ", measurement_packet.sample_id, int(packet.time * 1000)
        sys.stdout.flush()
