import socket
from scapy.all import *
from packet.MeasurementPacket import MeasurementPacket


class UdpPingResponder(object):

    def __init__(self, self_host, self_port, measurement_id):
        self.measurement_id = measurement_id

        self.self_host = self_host
        self.self_port = self_port
        self.proto = UDP

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self_host, self_port))

    def run(self):
        while True:
            data, addr = self.socket.recvfrom(64 * 1024)
            measurement_packet = MeasurementPacket.from_binary(data)
            print "responder got: ", measurement_packet.isResponse, measurement_packet.measurement_id, measurement_packet.sample_id
            self.socket.sendto(data, addr)
