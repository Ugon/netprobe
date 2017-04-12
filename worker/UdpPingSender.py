import socket
import time
from scapy.all import *
from packet.MeasurementPacket import MeasurementPacket
from uuid import *
from threading import Thread, Event
import sys


class UdpPingSender(object):

    def __init__(self, self_host, self_port, target_host, target_port, message_interval, measurement_id):
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

    def _run(self):
        while not self._stop.is_set():
            try:
                measurement_packet = MeasurementPacket(False, uuid4(), uuid4())
                # print "sending: ", measurement_packet.isResponse, measurement_packet.measurement_id, measurement_packet.sample_id
                self.socket.sendto(measurement_packet.to_binary(), (self.target_host, self.target_port))
                time.sleep(self.message_interval)
            except:
                print "thats not gone well"

        self._stop.clear()
        self.thread = None

    def async_start(self):
        if self.thread is not None:
            return False
        else:
            self.thread = Thread(target=self._run)
            self.thread.start()
            return True

    def stop(self):
        if self.thread is None:
            raise Exception("cant stop what is stopped")
        else:
            self._stop.set()


    def persist(self, packet):
        measurement_packet = MeasurementPacket.from_binary(packet[UDP].payload.load)
        print "SENDER:    ", measurement_packet.sample_id
        sys.stdout.flush()




