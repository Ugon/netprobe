package packet;

import java.util.UUID;

/**
 * @author Wojciech Pachuta.
 */
public class UDPPingPacket extends MeasurementPacket {

    public UDPPingPacket(boolean isResponse, UUID sampleId) {
        super(isResponse, MeasurementType.UDP_PING, sampleId);
    }

}
