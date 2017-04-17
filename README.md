# netprobe

```
sudo docker build -t netprobe .
sudo docker run --network="host" -e NET_INTERFACE=<your_interface> netprobe
```


## pomiar UDP ping

1) rozpoczęcie nasłuchiwania na hoście docelowym
`POST 192.168.0.15:5000/measurement/udp/responder/505e0c51-3ece-4ddf-93ec-e164ae346e47?self_port=40001`

2) rozpoczęcie nadawania na hoście źródłowym
`POST 192.168.0.2:5000/measurement/udp/sender/505e0c51-3ece-4ddf-93ec-e164ae346e47?self_port=40000&target_address=192.168.0.15&target_port=40001&interval_ms=1`

3) zebranie wyników z hosta docelowego
`GET 192.168.0.15:5000/measurement/udp/responder/505e0c51-3ece-4ddf-93ec-e164ae346e47`
`[{"timestamp": 1492457001178, "sample_id": "81b6ab86-eedb-4083-8523-bb1942116d6c"}]`

4) zebranie wyników z hosta źródłowego
`GET 192.168.0.2:5000/measurement/udp/sender/505e0c51-3ece-4ddf-93ec-e164ae346e47`
`[{"timestamp": 1492457001111, "sample_id": "81b6ab86-eedb-4083-8523-bb1942116d6c"}]`

5) zakończenie pomiarów na hoście źródłowym
`DELETE 192.168.0.2:5000/measurement/udp/sender/505e0c51-3ece-4ddf-93ec-e164ae346e47`

6) zakończenie pomiarów na hoście docelowym
`DELETE 192.168.0.15:5000/measurement/udp/responder/505e0c51-3ece-4ddf-93ec-e164ae346e47`

*) w tym przypadku sample-id to jest losowy UUID.



## pomiar TCP 3-way-handshake

1) rozpoczęcie nasłuchiwania na hoście docelowym
`POST 192.168.0.15:5000/measurement/tcp/server/505e0c51-3ece-4ddf-93ec-e164ae346e47?self_port=40001`

2) rozpoczęcie nadawania na hoście źródłowym
`POST 192.168.0.2:5000/measurement/tcp/client/505e0c51-3ece-4ddf-93ec-e164ae346e47?self_port=40000&target_address=192.168.0.15&target_port=40001&interval_ms=1`

3) zebranie wyników z hosta docelowego
`GET 192.168.0.15:5000/measurement/tcp/server/505e0c51-3ece-4ddf-93ec-e164ae346e47`

4) zebranie wyników z hosta źródłowego
`GET 192.168.0.2:5000/measurement/tcp/client/505e0c51-3ece-4ddf-93ec-e164ae346e47`

5) zakończenie pomiarów na hoście źródłowym
`DELETE 192.168.0.2:5000/measurement/tcp/client/505e0c51-3ece-4ddf-93ec-e164ae346e47`

6) zakończenie pomiarów na hoście docelowym
`DELETE 192.168.0.15:5000/measurement/tcp/server/505e0c51-3ece-4ddf-93ec-e164ae346e47`

*) w tym przypadku sample-id to jest SEQ z pakietow TCP. Zazwyczaj będą unikalne, ale tak być nie musi. Najbezpieczniej matchować po sample-id ale tylko te, które sa blisko siebie w czasie (do paru sekund).

<!--`sudo pip install scapy==2.2.0-dev`-->