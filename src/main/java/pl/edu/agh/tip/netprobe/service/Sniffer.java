package pl.edu.agh.tip.netprobe.service;

import org.jnetpcap.Pcap;
import org.jnetpcap.packet.JPacket;
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
        Pcap pcap = Pcap.openLive(networkInterface, 64 * 1024, Pcap.MODE_PROMISCUOUS, 1000, new StringBuilder());
        pcap.loop(-1, JProtocol.UDP_ID, (PcapPacketHandler<Object>) (pcapPacket, o) -> handlePacket(pcapPacket), null);
    }

    private void handlePacket(PcapPacket pcapPacket) {
        System.out.println(pcapPacket); //todo: <- to jest zjebane
        System.out.println(pcapPacket.getCaptureHeader().timestampInMicros());
    }

    private void handlePacket(JPacket jPacket) {
        System.out.println(jPacket.getUTF8String(0, 10000));
        System.out.println(jPacket.getCaptureHeader().timestampInMicros());
    }

}
