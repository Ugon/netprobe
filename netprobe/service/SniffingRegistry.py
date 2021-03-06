from scapy.all import *
from threading import Lock


class SniffingRegistry(object):

    def __init__(self):
        self.lock = Lock()

        self.senders = {}
        self.senders_self_ports = []

        self.responders = {}
        self.responders_self_ports = []

        self.receivers = {}
        self.receivers_self_ports = []

    def register_sender(self, measurement_id, sender):
        self.lock.acquire()
        try:
            self.senders[measurement_id] = sender
            self.senders_self_ports.append(sender.self_port)
        finally:
            self.lock.release()

    def get_sender(self, measurement_id):
        self.lock.acquire()
        try:
            sender = self.senders[measurement_id]
        finally:
            self.lock.release()
        return sender

    def remove_sender(self, measurement_id):
        self.lock.acquire()
        try:
            self.senders_self_ports.remove(self.senders[measurement_id].self_port)
            del self.senders[measurement_id]
        finally:
            self.lock.release()

    def register_responder(self, measurement_id, responder):
        self.lock.acquire()
        try:
            self.responders[measurement_id] = responder
            self.responders_self_ports.append(responder.self_port)
        finally:
            self.lock.release()

    def get_responder(self, measurement_id):
        self.lock.acquire()
        try:
            responder = self.responders[measurement_id]
        finally:
            self.lock.release()
        return responder

    def remove_responder(self, measurement_id):
        self.lock.acquire()
        try:
            self.responders_self_ports.append(self.responders[measurement_id].self_port)
            del self.responders[measurement_id]
        finally:
            self.lock.release()

    def register_receiver(self, measurement_id, receiver):
        self.lock.acquire()
        try:
            self.receivers[measurement_id] = receiver
            self.receivers_self_ports.append(receiver.self_port)
        finally:
            self.lock.release()

    def get_receiver(self, measurement_id):
        self.lock.acquire()
        try:
            receiver = self.receivers[measurement_id]
        finally:
            self.lock.release()
        return receiver

    def remove_receiver(self, measurement_id):
        self.lock.acquire()
        try:
            self.receivers_self_ports.remove(self.receivers[measurement_id].self_port)
            del self.receivers[measurement_id]
        finally:
            self.lock.release()

    def get_worker_for_packet(self, packet):
        for key, value in self.senders.iteritems():
            if value.proto in packet:
                if ICMP in packet:
                    if packet[IP].src == value.self_host and packet[ICMP].type == 8 and packet[ICMP].id == value.measurement_id:
                        return value
                elif IP in packet and packet[IP].src == value.self_host and packet[IP].sport == value.self_port:
                    return value

        for key, value in self.responders.iteritems():
            if value.proto in packet:
                if IP in packet and packet[IP].dst == value.self_host and packet[IP].dport == value.self_port:
                    return value

        for key, value in self.receivers.iteritems():
            if value.proto in packet:
                if ICMP in packet:
                    if packet[IP].dst == value.self_host and packet[ICMP].type == value.icmp_type:
                        return value
                elif IP in packet and packet[IP].dst == value.self_host and packet[IP].dport == value.self_port:
                    return value

        return None
