from worker.UdpPingSender import UdpPingSender
from worker.UdpPingResponder import UdpPingResponder
from service.SniffingRegistry import SniffingRegistry
from service.MeasurementService import MeasurementService
from service.Sniffer import Sniffer

from pymongo import MongoClient
from dao.MongoDao import MongoDao
from threading import Thread

from scapy.all import *


mongo_client = MongoClient()
udp_sender_dao = MongoDao(mongo_client, 'Netprobe', 'UdpSender')
udp_responder_dao = MongoDao(mongo_client, 'Netprobe', 'UdpResponder')


sniffing_registry = SniffingRegistry()
service = MeasurementService("127.0.0.1", sniffing_registry, udp_sender_dao, udp_responder_dao)

sniffer = Sniffer(sniffing_registry, "lo")
sniffer.async_start()

service.start_udp_sender(40000, "127.0.0.2", 40001, 1, "measureid")
service.start_udp_responder(40001, "measureid")


