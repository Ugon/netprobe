package service;

import org.jnetpcap.Pcap;
import org.jnetpcap.packet.PcapPacket;
import org.jnetpcap.packet.PcapPacketHandler;
import org.jnetpcap.protocol.JProtocol;

import java.io.IOException;

/**
 * @author Wojciech Pachuta.
 */
public class Sniffer implements Runnable {

    private final String networkInterface;

    public Sniffer(String networkInterface) throws IOException {
        this.networkInterface = networkInterface;
    }

    @Override
    public void run() {
        Pcap pcap = Pcap.openLive(networkInterface, 2048, Pcap.MODE_PROMISCUOUS, 1000, new StringBuilder());
        pcap.loop(-1, JProtocol.UDP_ID, (PcapPacketHandler<Object>) (pcapPacket, o) -> handlePacket(pcapPacket), null);
    }

    private void handlePacket(PcapPacket pcapPacket) {
        System.out.println(pcapPacket);
        System.out.println(pcapPacket.getCaptureHeader().timestampInMicros());
    }

}
