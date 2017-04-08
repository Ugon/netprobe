package pl.edu.agh.tip.netprobe;

import pl.edu.agh.tip.netprobe.service.MeasurementService;
import pl.edu.agh.tip.netprobe.service.Sniffer;

import java.io.IOException;

/**
 * @author Wojciech Pachuta.
 */
public class Main {
    public static void main(String[] args) throws IOException {
        System.setProperty("java.library.path", "/usr/lib/x86_64-linux-gnu:/home/ugon/development/projects/netprobe/lib/jnetpcap-1.3.0/libjnetpcap.so");
//        new Thread(new Sniffer("lo")).start();
        MeasurementService measurementService = new MeasurementService();
//        measurementService.startUDPPingResponder(40000);
//        measurementService.startUDPPingSender(40001, InetAddress.getByName("192.168.0.2"), 40000, 1000);
        new Sniffer("wlan0").run();
    }
}
