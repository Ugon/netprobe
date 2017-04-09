package pl.edu.agh.tip.netprobe.packet;

import java.nio.ByteBuffer;
import java.util.UUID;

/**
 * @author Wojciech Pachuta.
 */
public class MeasurementPacket {
    public static final int SIZE = 1 + 1 + 16;

    private final boolean isResponse;
    private final MeasurementType measurementType;
    private final UUID sampleId;

    public MeasurementPacket(boolean isResponse, MeasurementType measurementType, UUID sampleId) {
        this.isResponse = isResponse;
        this.measurementType = measurementType;
        this.sampleId = sampleId;
    }

    public boolean isResponse() {
        return isResponse;
    }

    public UUID getSampleId() {
        return sampleId;
    }

    public MeasurementType getMeasurementType() {
        return measurementType;
    }

    public MeasurementPacket toResponse() {
        if (isResponse) {
            throw new IllegalStateException();
        } else {
            return new MeasurementPacket(true, measurementType, sampleId);
        }

    }

    public byte[] asBytes() {
        ByteBuffer bb = ByteBuffer.wrap(new byte[SIZE]);
        bb.put(isResponse ? (byte) 1 : (byte) 0);
        bb.put(measurementType.getNumber());
        bb.putLong(sampleId.getMostSignificantBits());
        bb.putLong(sampleId.getLeastSignificantBits());

        return bb.array();
    }

    public static MeasurementPacket fromBytes(byte[] bytes) {
        ByteBuffer byteBuffer = ByteBuffer.wrap(bytes);
        boolean isResponse = byteBuffer.get() != 0;
        byte measurementType = byteBuffer.get();
        Long high = byteBuffer.getLong();
        Long low = byteBuffer.getLong();

        return new MeasurementPacket(isResponse, MeasurementType.forNumber(measurementType), new UUID(high, low));
    }

}
