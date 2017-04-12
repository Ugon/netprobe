import socket
from scapy.all import *
from packet.MeasurementPacket import MeasurementPacket
import select
import sys

from threading import Thread, Event




class UdpPingResponder(object):

    def __init__(self, self_host, self_port, measurement_id):
        self.measurement_id = measurement_id

        self.self_host = self_host
        self.self_port = self_port
        self.proto = UDP

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setblocking(0)
        self.socket.bind((self_host, self_port))

        self.thread = None
        self._stop = Event()

    def _run(self):
        while not self._stop.is_set():
            ready = select.select([self.socket], [], [], 1)
            if ready[0]:
                data, addr = self.socket.recvfrom(64 * 1024)
                # measurement_packet = MeasurementPacket.from_binary(data)
                # print "responder got: ", measurement_packet.isResponse, measurement_packet.measurement_id, measurement_packet.sample_id
                self.socket.sendto(data, addr)

        self._stop.clear()
        self.thread = None

    def async_start(self):
        if self.thread is not None:
            raise Exception("cant start what is started")
        else:
            self.thread = Thread(target=self._run)
            self.thread.start()

    def stop(self):
        if self.thread is None:
            raise Exception("cant stop what is stopped")
        else:
            self._stop.set()

    def persist(self, packet):
        measurement_packet = MeasurementPacket.from_binary(packet[UDP].payload.load)
        print "RESPONDER: ", measurement_packet.sample_id
        sys.stdout.flush()
