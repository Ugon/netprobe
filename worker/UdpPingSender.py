import socket
import time
from scapy.all import *
from packet.MeasurementPacket import MeasurementPacket
from uuid import *
from threading import Thread, Event
import sys
from worker.AbstractWorker import AbstractWorker

class UdpPingSender(AbstractWorker):

    def __init__(self, self_host, self_port, target_host, target_port, message_interval, measurement_id):
        super(UdpPingSender, self).__init__()
        self.measurement_id = measurement_id

        self.self_host = self_host
        self.self_port = self_port
        self.proto = UDP

        self.target_host = target_host
        self.target_port = target_port
        self.message_interval = message_interval

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self_host, self_port))

        self.thread = None
        self._stop = Event()

    def loop_iteration(self):
        try:
            measurement_packet = MeasurementPacket(False, uuid4(), uuid4())
            # print "sending: ", measurement_packet.isResponse, measurement_packet.measurement_id, measurement_packet.sample_id
            self.socket.sendto(measurement_packet.to_binary(), (self.target_host, self.target_port))
            time.sleep(self.message_interval)
        except:
            print "thats not gone well"

    def persist_packet(self, packet):
        measurement_packet = MeasurementPacket.from_binary(packet[UDP].payload.load)
        print "SENDER:    ", measurement_packet.sample_id
        sys.stdout.flush()




