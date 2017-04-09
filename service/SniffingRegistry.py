from threading import Lock
from scapy.all import *


class SniffingRegistry(object):

    def __init__(self):
        self.lock = Lock()

        self.senders = {}
        self.senders_self_ports = []

        self.responders = {}
        self.responders_self_ports = []

    def register_sender(self, id, sender):
        self.lock.acquire()
        self.senders[id] = sender
        self.senders_self_ports.append(sender.self_port)
        self.lock.release()

    def remove_sender(self, id):
        self.lock.acquire()
        self.senders_self_ports.remove(self.senders[id].self_port)
        del self.senders[id]
        self.lock.release()

    def register_responder(self, id, responder):
        self.lock.acquire()
        self.responders[id] = responder
        self.responders_self_ports.append(responder.self_port)
        self.lock.release()

    def remove_responder(self, id):
        self.lock.acquire()
        self.responders_self_ports.append(self.responders[id].self_port)
        del self.responders[id]
        self.lock.release()

    def get_worker_for_packet(self, packet):
        for key, value in self.senders.iteritems():
            if value.proto in packet:
                if IP in packet and packet[IP].src == value.self_host and packet[IP].sport == value.self_port:
                    return value

        for key, value in self.responders.iteritems():
            if value.proto in packet:
                if IP in packet and packet[IP].dst == value.self_host and packet[IP].dport == value.self_port:
                    return value

        return None
