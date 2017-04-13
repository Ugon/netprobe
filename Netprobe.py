from flask import Flask, request
from service.SniffingRegistry import SniffingRegistry
from service.MeasurementService import MeasurementService
from service.Sniffer import Sniffer
import traceback
from pymongo import MongoClient
from dao.MongoDao import MongoDao
from uuid import UUID
import json
app = Flask(__name__)

mongo_client = MongoClient()
udp_sender_dao = MongoDao(mongo_client, 'Netprobe', 'UdpSender')
udp_responder_dao = MongoDao(mongo_client, 'Netprobe', 'UdpResponder')


sniffing_registry = SniffingRegistry()
service = MeasurementService("127.0.0.1", sniffing_registry, udp_sender_dao, udp_responder_dao)

sniffer = Sniffer(sniffing_registry, "lo")
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

        #QUERY PARAMS:
        self_port = int(request.args.get('self_port'))
        target_address = request.args.get('target_address')
        target_port = int(request.args.get('target_port'))
        interval_ms = int(request.args.get('interval_ms'))

        service.start_udp_sender(self_port, target_address, target_port, interval_ms, measurement_id)
        return "ok", 200
    except:
        return traceback.format_exc(), 400


@app.route('/measurement/udp/sender/<measurement_uuid>', methods=['DELETE'])
def stop_udp_sender(measurement_uuid):
    try:
        measurement_id = UUID(measurement_uuid)
        service.stop_udp_sender(measurement_id)
        return "ok", 200
    except:
        return traceback.format_exc(), 400


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

        #QUERY PARAMS:
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

app.run()
