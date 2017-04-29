from worker.UdpPingSender import UdpPingSender
from worker.UdpPingResponder import UdpPingResponder
from worker.UdpPingReceiver import UdpPingReceiver
from worker.TcpServer import TcpServer
from worker.TcpClient import TcpClient
from worker.PingSender import PingSender
from worker.PingReceiver import PingReceiver
from worker.PingResponder import PingResponder


class MeasurementService(object):
    def __init__(self, self_address, sniffing_registry, udp_sender_dao, udp_responder_dao, udp_receiver_dao,
                 tcp_server_dao, tcp_client_dao, icmp_sender_dao, icmp_receiver_dao, icmp_responder_dao):
        self.self_address = self_address
        self.sniffing_registry = sniffing_registry

        self.udp_sender_dao = udp_sender_dao
        self.udp_responder_dao = udp_responder_dao
        self.udp_receiver_dao = udp_receiver_dao
        self.tcp_server_dao = tcp_server_dao
        self.tcp_client_dao = tcp_client_dao
        self.icmp_sender_dao = icmp_sender_dao
        self.icmp_receiver_dao = icmp_receiver_dao
        self.icmp_responder_dao = icmp_responder_dao

    def start_udp_sender_and_receiver(self, self_port, target_address, target_port, interval_ms, measurement_id):
        sender = UdpPingSender(self.self_address, self_port, target_address, target_port, interval_ms, measurement_id,
                               self.udp_sender_dao)
        receiver = UdpPingReceiver(self.self_address, self_port, sender.socket, measurement_id, self.udp_receiver_dao)
        self.sniffing_registry.register_sender(measurement_id, sender)
        self.sniffing_registry.register_receiver(measurement_id, receiver)
        return sender.async_start() and receiver.async_start()

    def stop_udp_sender_and_receiver(self, measurement_id):
        sender = self.sniffing_registry.get_sender(measurement_id)
        receiver = self.sniffing_registry.get_receiver(measurement_id)
        if sender is not None:
            sender.stop()
            receiver.stop()
            self.sniffing_registry.remove_sender(measurement_id)
            self.sniffing_registry.remove_receiver(measurement_id)
            return True
        else:
            return False

    def start_udp_responder(self, self_port, measurement_id):
        responder = UdpPingResponder(self.self_address, self_port, measurement_id, self.udp_responder_dao)
        self.sniffing_registry.register_responder(measurement_id, responder)
        return responder.async_start()

    def stop_udp_responder(self, measurement_id):
        responder = self.sniffing_registry.get_responder(measurement_id)
        if responder is not None:
            responder.stop()
            self.sniffing_registry.remove_responder(measurement_id)
            return True
        else:
            return False

    def start_tcp_server(self, self_port, measurement_id):
        server = TcpServer(self.self_address, self_port, measurement_id, self.tcp_server_dao)
        self.sniffing_registry.register_receiver(measurement_id, server)
        return server.async_start()

    def stop_tcp_server(self, measurement_id):
        server = self.sniffing_registry.get_receiver(measurement_id)
        if server is not None:
            server.stop()
            self.sniffing_registry.remove_receiver(measurement_id)
            return True
        else:
            return False

    def start_tcp_client(self, self_port, target_address, target_port, interval_ms, measurement_id):
        client = TcpClient(self.self_address, self_port, target_address, target_port, interval_ms, measurement_id, self.tcp_client_dao)
        self.sniffing_registry.register_sender(measurement_id, client)
        return client.async_start()

    def stop_tcp_client(self, measurement_id):
        client = self.sniffing_registry.get_sender(measurement_id)
        if client is not None:
            client.stop()
            self.sniffing_registry.remove_sender(measurement_id)
            return True
        else:
            return False

    def start_icmp_receiver(self):
        receiver = PingReceiver(self.self_address, self.icmp_receiver_dao)
        self.sniffing_registry.register_receiver("icmp_ping_receiver", receiver)
        return receiver.async_start()

    def start_icmp_responder(self):
        responder = PingResponder(self.self_address, self.icmp_responder_dao)
        self.sniffing_registry.register_receiver("icmp_ping_responder", responder)
        return responder.async_start()

    def start_icmp_sender(self, target_address, interval_ms, measurement_id):
        sender = PingSender(self.self_address, target_address, interval_ms, measurement_id, self.icmp_sender_dao)
        self.sniffing_registry.register_sender(measurement_id, sender)
        return sender.async_start()

    def stop_icmp_sender(self, measurement_id):
        sender = self.sniffing_registry.get_sender(measurement_id)
        if sender is not None:
            sender.stop()
            self.sniffing_registry.remove_sender(measurement_id)
            return True
        else:
            return False

    def stop_all(self):
        for k, v in self.sniffing_registry.senders.copy().iteritems():
            v.stop()
            self.sniffing_registry.remove_sender(k)
        for k, v in self.sniffing_registry.responders.copy().iteritems():
            v.stop()
            self.sniffing_registry.remove_responder(k)
        for k, v in self.sniffing_registry.receivers.copy().iteritems():
            v.stop()
            self.sniffing_registry.remove_receiver(k)
