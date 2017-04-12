from worker.UdpPingSender import UdpPingSender
from worker.UdpPingResponder import UdpPingResponder


class MeasurementService(object):
    def __init__(self, self_address, sniffing_registry):
        self.self_address = self_address
        self.sniffing_registry = sniffing_registry

    def start_udp_sender(self, self_port, target_address, target_port, interval_ms, measurement_id):
        sender = UdpPingSender(self.self_address, self_port, target_address, target_port, interval_ms, measurement_id)
        self.sniffing_registry.register_sender(measurement_id, sender)
        return sender.async_start()

    def stop_udp_sender(self, measurement_id):
        sender = self.sniffing_registry.get_sender(measurement_id)
        if sender is not None:
            sender.stop()
            self.sniffing_registry.remove_sender(measurement_id)
            return True
        else:
            return False

    def start_udp_responder(self, self_port, measurement_id):
        responder = UdpPingResponder(self.self_address, self_port, measurement_id)
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
