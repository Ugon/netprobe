from uuid import *

import bitstring


class MeasurementPacket(object):
    def __init__(self, isResponse, measurement_id, sample_id):
        self.isResponse = isResponse
        self.measurement_id = measurement_id
        self.sample_id = sample_id

    def to_binary(self):
        return bitstring.pack('bool, hex:128, hex:128, pad:7', self.isResponse, self.measurement_id.hex,
                              self.sample_id.hex).bytes

    @staticmethod
    def from_binary(binary):
        result = bitstring.BitArray(bytes=binary).unpack('bool, hex:128, hex:128')
        return MeasurementPacket(result[0], UUID(hex=result[1]), UUID(hex=result[2]))
