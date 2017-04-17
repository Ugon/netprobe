import json
import sys
import traceback
from uuid import UUID

import netifaces as ni
from flask import Flask, request
from pymongo import MongoClient

from dao.MongoDao import MongoDao
from service.MeasurementService import MeasurementService
from service.Sniffer import Sniffer
from service.SniffingRegistry import SniffingRegistry

interface = sys.argv[1]

self_ip = ni.ifaddresses(interface)[2][0]['addr']
print self_ip
self_ip = "127.0.0.1"

app = Flask(__name__)

# mongo_client = MongoClient(host=self_ip, port=50000)
mongo_client = MongoClient()
udp_sender_dao = MongoDao(mongo_client, 'Netprobe', 'UdpSender')
udp_responder_dao = MongoDao(mongo_client, 'Netprobe', 'UdpResponder')
udp_receiver_dao = MongoDao(mongo_client, 'Netprobe', 'UdpReceiver')
tcp_server_dao = MongoDao(mongo_client, 'Netprobe', 'TcpServer')
tcp_client_dao = MongoDao(mongo_client, 'Netprobe', 'TcpClient')

sniffing_registry = SniffingRegistry()
service = MeasurementService(self_ip, sniffing_registry, udp_sender_dao, udp_responder_dao, udp_receiver_dao,
                             tcp_server_dao, tcp_client_dao)

sniffer = Sniffer(sniffing_registry, interface)
sniffer.async_start()


@app.route('/measurement/udp/sender/<measurement_uuid>', methods=['GET'])
def get_udp_sender_results(measurement_uuid):
    try:
        measurement_id = UUID(measurement_uuid)
        result = udp_sender_dao.get_all(measurement_id)
        return json.dumps(result), 200
    except:
        return traceback.format_exc(), 400

@app.route('/measurement/udp/sender/<measurement_uuid>', methods=['POST'])
def start_udp_sender(measurement_uuid):
    try:
        measurement_id = UUID(measurement_uuid)

        # QUERY PARAMS:
        self_port = int(request.args.get('self_port'))
        target_address = request.args.get('target_address')
        target_port = int(request.args.get('target_port'))
        interval_ms = int(request.args.get('interval_ms'))

        service.start_udp_sender_and_receiver(self_port, target_address, target_port, interval_ms, measurement_id)
        return "ok", 200
    except:
        return traceback.format_exc(), 400


@app.route('/measurement/udp/sender/<measurement_uuid>', methods=['DELETE'])
def stop_udp_sender(measurement_uuid):
    try:
        measurement_id = UUID(measurement_uuid)
        service.stop_udp_sender_and_receiver(measurement_id)
        return "ok", 200
    except:
        return traceback.format_exc(), 400

#########################################################################################

@app.route('/measurement/udp/responder/<measurement_uuid>', methods=['GET'])
def get_udp_responder_results(measurement_uuid):
    try:
        measurement_id = UUID(measurement_uuid)
        result = udp_responder_dao.get_all(measurement_id)
        return json.dumps(result), 200
    except:
        return traceback.format_exc(), 400


@app.route('/measurement/udp/responder/<measurement_uuid>', methods=['POST'])
def start_udp_responder(measurement_uuid):
    try:
        measurement_id = UUID(measurement_uuid)

        # QUERY PARAMS:
        self_port = int(request.args.get('self_port'))

        service.start_udp_responder(self_port, measurement_id)
        return "ok", 200
    except:
        return traceback.format_exc(), 400


@app.route('/measurement/udp/responder/<measurement_uuid>', methods=['DELETE'])
def stop_udp_responder(measurement_uuid):
    try:
        measurement_id = UUID(measurement_uuid)
        service.stop_udp_responder(measurement_id)
        return "ok", 200
    except:
        return traceback.format_exc(), 400

#########################################################################################

@app.route('/measurement/tcp/client/<measurement_uuid>', methods=['GET'])
def get_tcp_client_results(measurement_uuid):
    try:
        measurement_id = UUID(measurement_uuid)
        result = tcp_client_dao.get_all(measurement_id)
        return json.dumps(result), 200
    except:
        return traceback.format_exc(), 400


@app.route('/measurement/tcp/client/<measurement_uuid>', methods=['POST'])
def start_tcp_client(measurement_uuid):
    try:
        measurement_id = UUID(measurement_uuid)

        # QUERY PARAMS:
        self_port = int(request.args.get('self_port'))
        target_address = request.args.get('target_address')
        target_port = int(request.args.get('target_port'))
        interval_ms = int(request.args.get('interval_ms'))

        service.start_tcp_client(self_port, target_address, target_port, interval_ms, measurement_id)
        return "ok", 200
    except:
        return traceback.format_exc(), 400


@app.route('/measurement/tcp/client/<measurement_uuid>', methods=['DELETE'])
def stop_tcp_client(measurement_uuid):
    try:
        measurement_id = UUID(measurement_uuid)
        service.stop_tcp_client(measurement_id)
        return "ok", 200
    except:
        return traceback.format_exc(), 400


#########################################################################################

@app.route('/measurement/tcp/server/<measurement_uuid>', methods=['GET'])
def get_tcp_server_results(measurement_uuid):
    try:
        measurement_id = UUID(measurement_uuid)
        result = tcp_server_dao.get_all(measurement_id)
        return json.dumps(result), 200
    except:
        return traceback.format_exc(), 400


@app.route('/measurement/tcp/server/<measurement_uuid>', methods=['POST'])
def start_tcp_server(measurement_uuid):
    try:
        measurement_id = UUID(measurement_uuid)

        # QUERY PARAMS:
        self_port = int(request.args.get('self_port'))

        service.start_tcp_server(self_port, measurement_id)
        return "ok", 200
    except:
        return traceback.format_exc(), 400


@app.route('/measurement/tcp/server/<measurement_uuid>', methods=['DELETE'])
def stop_tcp_server(measurement_uuid):
    try:
        measurement_id = UUID(measurement_uuid)
        service.stop_tcp_server(measurement_id)
        return "ok", 200
    except:
        return traceback.format_exc(), 400

#########################################################################################

app.run(self_ip, 5000)
