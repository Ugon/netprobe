package pl.edu.agh.tip.netprobe.packet;

/**
 * @author Wojciech Pachuta.
 */
public enum MeasurementType {
    UDP_PING((byte) 1),
    TCP_CONNECTION((byte) 2);

    private final byte number;

    MeasurementType(byte number) {
        this.number = number;
    }

    public byte getNumber() {
        return number;
    }

    public static MeasurementType forNumber(byte number) {
        switch (number) {
            case 1: return UDP_PING;
            case 2: return TCP_CONNECTION;
            default: throw new IllegalArgumentException();
        }
    }
}
