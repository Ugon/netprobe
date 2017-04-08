package service;

import runnables.UDPPingResponder;
import runnables.UDPPingSender;

import java.net.InetAddress;
import java.net.SocketException;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;
import java.util.concurrent.*;

/**
 * @author Wojciech Pachuta.
 */
public class MeasurementService {

    private final Map<UUID, ScheduledFuture> runningSenders;
    private final Map<UUID, Thread> runningResponders;

    private final ScheduledExecutorService executor;

    public MeasurementService() {
        this.executor = Executors.newScheduledThreadPool(4);
        runningSenders = new ConcurrentHashMap<>();
        runningResponders = new ConcurrentHashMap<>();
    }

    public UUID startUDPPingSender(int port, InetAddress targetAddress, int targetPort, int intervalMS) throws SocketException {
        UDPPingSender sender = new UDPPingSender(port, targetAddress, targetPort);
        ScheduledFuture<?> scheduledFuture = executor.schedule(sender, intervalMS, TimeUnit.MILLISECONDS);
        UUID uuid = UUID.randomUUID();
        runningSenders.put(uuid, scheduledFuture);
        return uuid;
    }

    public void cancelUDPPingSender(UUID uuid) {
        Optional.ofNullable(runningSenders.remove(uuid)).ifPresent(x -> x.cancel(true));
    }

    public UUID startUDPPingResponder(int port) throws SocketException {
        UDPPingResponder udpPingResponder = new UDPPingResponder(port);
        Thread thread = new Thread(udpPingResponder);
        thread.start();
        UUID uuid = UUID.randomUUID();
        runningResponders.put(uuid, thread);
        return uuid;
    }

    public void cancelUDPPingResponder(UUID uuid) {
        Optional.ofNullable(runningResponders.remove(uuid)).ifPresent(Thread::stop);
    }



}
