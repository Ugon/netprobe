package runnables;

import packet.UDPPingPacket;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.util.UUID;

/**
 * @author Wojciech Pachuta.
 */
public class UDPPingSender implements Runnable {
    private final DatagramSocket udpSocket;
    private final InetAddress targeAddress;
    private final int targetPort;

    public UDPPingSender(int selfPort, InetAddress targetAddress, int targetPort) throws SocketException {
        this.udpSocket = new DatagramSocket(selfPort);
        this.targeAddress = targetAddress;
        this.targetPort = targetPort;
    }

    @Override
    public void run() {
        try {
            UDPPingPacket msg = new UDPPingPacket(false, UUID.randomUUID());
            DatagramPacket datagramPacket = new DatagramPacket(msg.asBytes(), UDPPingPacket.SIZE, targeAddress, targetPort);
            udpSocket.send(datagramPacket);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
