package pl.edu.agh.tip.netprobe.runnables;

import pl.edu.agh.tip.netprobe.packet.MeasurementPacket;
import pl.edu.agh.tip.netprobe.packet.UDPPingPacket;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;

/**
 * @author Wojciech Pachuta.
 */
public class UDPPingResponder implements Runnable {

    private final DatagramSocket udpSocket;
    private byte[] dataBuffer = new byte[UDPPingPacket.SIZE];

    public UDPPingResponder(int port) throws SocketException {
        udpSocket = new DatagramSocket(port);
    }

    @Override
    public void run() {
        while (true) {
            try {
                DatagramPacket receivePacket = new DatagramPacket(dataBuffer, MeasurementPacket.SIZE);
                udpSocket.receive(receivePacket);

                MeasurementPacket request = MeasurementPacket.fromBytes(receivePacket.getData());
                InetAddress senderAddress = receivePacket.getAddress();
                int senderPort = receivePacket.getPort();

                //todo: remove or log
                System.out.println(System.currentTimeMillis() + " deflecting pl.edu.agh.tip.netprobe.packet: " + request.getSampleId());

                DatagramPacket sendPacket = new DatagramPacket(request.toResponse().asBytes(), MeasurementPacket.SIZE, senderAddress, senderPort);
                udpSocket.send(sendPacket);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}
