from threading import Lock


class SniffingRegistry(object):

    def __init__(self):
        self.lock = Lock()

        self.senders = {}
        self.senders_self_ports = []

        self.responders = {}
        self.responders_self_ports = []

    def register_sender(self, measurement_id, sender):
        self.lock.acquire()
        self.senders[measurement_id] = sender
        self.senders_self_ports.append(sender.self_port)
        self.lock.release()

    def get_sender(self, measurement_id):
        self.lock.acquire()
        sender = self.senders[measurement_id]
        self.lock.release()
        return sender

    def remove_sender(self, measurement_id):
        self.lock.acquire()
        self.senders_self_ports.remove(self.senders[measurement_id].self_port)
        del self.senders[measurement_id]
        self.lock.release()

    def register_responder(self, measurement_id, responder):
        self.lock.acquire()
        self.responders[measurement_id] = responder
        self.responders_self_ports.append(responder.self_port)
        self.lock.release()

    def get_responder(self, measurement_id):
        self.lock.acquire()
        responder = self.responders[measurement_id]
        self.lock.release()
        return responder

    def remove_responder(self, measurement_id):
        self.lock.acquire()
        self.responders_self_ports.append(self.responders[measurement_id].self_port)
        del self.responders[measurement_id]
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
