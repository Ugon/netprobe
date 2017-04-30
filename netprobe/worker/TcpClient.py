from scapy.all import *
from threading import Lock
from uuid import *

from packet.MeasurementPacket import MeasurementPacket
from worker.AbstractWorker import AbstractWorker


class TcpClient(AbstractWorker):
    def __init__(self, self_host, self_port, target_host, target_port, message_interval, measurement_id, dao):
        super(TcpClient, self).__init__()
        self.dao = dao
        self.measurement_id = measurement_id

        self.self_host = self_host
        self.self_port = self_port
        self.proto = TCP

        self.target_host = target_host
        self.target_port = target_port
        self.message_interval = message_interval

        self.lock = Lock()
        self.syn = None

    def loop_iteration(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.self_host, self.self_port))
        s.connect((self.target_host, self.target_port))
        measurement_packet = MeasurementPacket(False, self.measurement_id, uuid4())
        s.send(measurement_packet.to_binary())
        s.shutdown(socket.SHUT_WR)
        s.close()
        done = False
        while not done:
            self.lock.acquire()
            try:
                if self.syn is not None:
                    self.dao.insert(measurement_packet.measurement_id, self.syn[TCP].seq + 1, int(self.syn.time * 1000))
                    print "CLIENT:    ", self.syn[TCP].seq + 1, int(self.syn.time * 1000)
                    sys.stdout.flush()
                    done = True
            finally:
                self.lock.release()
        time.sleep(self.message_interval)

    def persist_packet(self, packet):
        if packet[TCP].flags == 2:
            self.lock.acquire()
            try:
                self.syn = packet
            finally:
                self.lock.release()
