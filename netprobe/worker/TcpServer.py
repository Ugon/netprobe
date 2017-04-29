import select
from scapy.all import *
from threading import Lock

from packet.MeasurementPacket import MeasurementPacket
from worker.AbstractWorker import AbstractWorker


class TcpServer(AbstractWorker):
    def __init__(self, self_host, self_port, measurement_id, dao):
        super(TcpServer, self).__init__()
        self.dao = dao
        self.measurement_id = measurement_id

        self.self_host = self_host
        self.self_port = self_port
        self.proto = TCP

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self_host, self_port))
        self.socket.listen(10)

        self.lock = Lock()
        self.ack = None

    def loop_iteration(self):
        ready = select.select([self.socket], [], [], 1)
        if ready[0]:
            client_socket, client_address = self.socket.accept()
            data = client_socket.recv(64 * 1024)
            client_socket.shutdown(socket.SHUT_WR)
            client_socket.close()
            measurement_packet = MeasurementPacket.from_binary(data)
            done = False
            while not done:
                self.lock.acquire()
                try:
                    if self.ack is not None:
                        self.dao.insert(measurement_packet.measurement_id, measurement_packet.sample_id, int(self.ack.time * 1000))
                        print "SERVER:    ", self.ack[TCP].seq, measurement_packet.sample_id, int(self.ack.time * 1000)
                        sys.stdout.flush()
                        done = True
                finally:
                    self.lock.release()

    def persist_packet(self, packet):
        if packet[TCP].flags == 16:
            self.lock.acquire()
            try:
                self.ack = packet
            finally:
                self.lock.release()
