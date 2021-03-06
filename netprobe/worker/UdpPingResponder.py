import select
from scapy.all import *

from packet.MeasurementPacket import MeasurementPacket
from worker.AbstractWorker import AbstractWorker


class UdpPingResponder(AbstractWorker):
    def __init__(self, self_host, self_port, measurement_id, dao):
        super(UdpPingResponder, self).__init__()
        self.dao = dao
        self.measurement_id = measurement_id

        self.self_host = self_host
        self.self_port = self_port
        self.proto = UDP

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setblocking(0)
        self.socket.bind((self_host, self_port))

    def loop_iteration(self):
        ready = select.select([self.socket], [], [], 1)
        if ready[0]:
            data, addr = self.socket.recvfrom(64 * 1024)
            # measurement_packet = MeasurementPacket.from_binary(data)
            # print "responder got: ", measurement_packet.isResponse, measurement_packet.measurement_id, measurement_packet.sample_id
            self.socket.sendto(data, addr)

    def persist_packet(self, packet):
        measurement_packet = MeasurementPacket.from_binary(packet[UDP].payload.load)
        self.dao.insert(measurement_packet.measurement_id, measurement_packet.sample_id, int(packet.time * 1000))
        print "RESPONDER: ", measurement_packet.sample_id, int(packet.time * 1000)
        sys.stdout.flush()
