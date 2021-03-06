from scapy.all import *
from uuid import *

from packet.MeasurementPacket import MeasurementPacket
from worker.AbstractWorker import AbstractWorker


class UdpPingSender(AbstractWorker):
    def __init__(self, self_host, self_port, target_host, target_port, message_interval, measurement_id, dao):
        super(UdpPingSender, self).__init__()
        self.dao = dao
        self.measurement_id = measurement_id

        self.self_host = self_host
        self.self_port = self_port
        self.proto = UDP

        self.target_host = target_host
        self.target_port = target_port
        self.message_interval = message_interval

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self_host, self_port))

    def loop_iteration(self):
        measurement_packet = MeasurementPacket(False, self.measurement_id, uuid4())
        self.socket.sendto(measurement_packet.to_binary(), (self.target_host, self.target_port))
        time.sleep(self.message_interval)

    def persist_packet(self, packet):
        measurement_packet = MeasurementPacket.from_binary(packet[UDP].payload.load)
        self.dao.insert(measurement_packet.measurement_id, measurement_packet.sample_id, int(packet.time * 1000))
        print "SENDER:    ", measurement_packet.sample_id, int(packet.time * 1000)
        sys.stdout.flush()
