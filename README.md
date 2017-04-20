# netprobe

## How to run

```
sudo docker build -t netprobe .
sudo docker run --network="host" -e NET_INTERFACE=<your_interface> netprobe
```


## Pomiar UDP ping
```
            source                          target 
              |                               |
  sender time |-------udp ping reguest------->| responder time
              |                               |
receiver time |<------udp ping response-------|
              |                               |
              
One way delay (source -> targer) = responder time - sender time
One way delay (target -> source) = receiver time - responder time
Two way delay = receiver time - sender time
```
Pakiety `udp ping request` i `udp ping response` zawierają pola `measurement_id` (uuid) i `sample_id` (uuid), 
dzięki którym można jednoznacznie połączyć zmierzone stemple czasowe w pary i obliczyć opóźnienia.


1) Rozpoczęcie nasłuchiwania na hoście docelowym
```
POST <target_ip>:5000/measurement/udp/responder/<measurement_uuid>
     ?self_port=<target_port>`
```
2) Rozpoczęcie nadawania na hoście źródłowym
```
POST <source_ip>:5000/measurement/udp/sender/<measurement_uuid>
     ?self_port=<source_port>
     &target_address=<target_ip>
     &target_port=<target_port>
     &interval_s=<interval>
```

3) Pobranie wyników z hosta docelowego (responder time)
```
GET <target_ip>:5000/measurement/udp/responder/<measurement_uuid>

Example response:
[{"timestamp": 1492457001178, "sample_id": "81b6ab86-eedb-4083-8523-bb1942116d6c"}]
```

4) Pobranie wyników z hosta źródłowego (sender time)
```
GET <source_ip>:5000/measurement/udp/sender/<measurement_uuid>

Example response:
[{"timestamp": 1492457001111, "sample_id": "81b6ab86-eedb-4083-8523-bb1942116d6c"}]
```

5) Pobranie wyników z hosta źródłowego (receiver time)
```
GET <source_ip>:5000/measurement/udp/receiver/<measurement_uuid>

Example response:
[{"timestamp": 1492457001151, "sample_id": "81b6ab86-eedb-4083-8523-bb1942116d6c"}]
```

6) zakończenie pomiarów na hoście źródłowym
```
DELETE <source_ip>:5000/measurement/udp/sender/<measurement_uuid>
```

7) zakończenie pomiarów na hoście docelowym
```
DELETE <target_ip>:5000/measurement/udp/responder/<measurement_uuid>
```


## Pomiar TCP 3-way-handshake
```
            client                          server 
              |                               |
  client time |-----SYN(SEQ)----------------->| 
              |                               |
              |<----SYN(SEQ+1); ACK(SEQ)------|
              |                               |
              |-----ACK(SEQ+1)--------------->| server time
              |                               |
              
3-way-handshake time = server time - client time
```
Po nawiązaniu połączenia klient wysyła do serwera wiadomość zawierającą `measurement_id` (uuid) i zamyka połączenie. 
`sample_id` pozwalającym na połączenie zmierzonych stempli czasowych w pary w tym przypadku jest `SEQ+1` (int).


1) Rozpoczęcie nasłuchiwania na hoście docelowym
```
POST <target_ip>:5000/measurement/tcp/server/<measurement_uuid>
     ?self_port=<target_port>`
```
2) Rozpoczęcie nadawania na hoście źródłowym
```
POST <source_ip>:5000/measurement/tcp/client/<measurement_uuid>
     ?self_port=<source_port>
     &target_address=<target_ip>
     &target_port=<target_port>
     &interval_s=<interval>
```

3) Pobranie wyników z hosta docelowego (server time)
```
GET <target_ip>:5000/measurement/tcp/server/<measurement_uuid>

Example response:
[{"timestamp": 1492457001178, "sample_id": 8562148}]
```

4) Pobranie wyników z hosta źródłowego (client time)
```
GET <source_ip>:5000/measurement/tcp/client/<measurement_uuid>

Example response:
[{"timestamp": 1492457001111, "sample_id": 8562148}]
```

5) zakończenie pomiarów na hoście źródłowym
```
DELETE <source_ip>:5000/measurement/tcp/client/<measurement_uuid>
```

6) zakończenie pomiarów na hoście docelowym
```
DELETE <target_ip>:5000/measurement/tcp/server/<measurement_uuid>
```


## Pomiar ICMP ping
```
            source                          target 
              |                               |
  sender time |------icmp ping reguest------->| responder time
              |                               |
receiver time |<-----icmp ping response-------|
              |                               |
              
One way delay (source -> targer) = responder time - sender time
One way delay (target -> source) = receiver time - responder time
Two way delay = receiver time - sender time
```
Pakiety `icmp ping request` i `icmp ping response` zawierają pola `id` (measurement_id, short) i `seq` (sample_id, short), 
dzięki którym można jednoznacznie połączyć zmierzone stemple czasowe w pary i obliczyć opóźnienia.

Hosty nie wymagają włączania nasłuchiwania - działa ono zawsze.

1) Rozpoczęcie nadawania na hoście źródłowym
```
POST <source_ip>:5000/measurement/icmp/sender/<measurement_short_id>
     ?target_address=<target_ip>
     &interval_s=<interval>
```

2) Pobranie wyników z hosta docelowego (responder time)
```
GET <target_ip>:5000/measurement/icmp/responder/<measurement_short_id>

Example response:
[{"timestamp": 1492457001178, "sample_id": 7}]
```

3) Pobranie wyników z hosta źródłowego (sender time)
```
GET <source_ip>:5000/measurement/icmp/sender/<measurement_short_id>

Example response:
[{"timestamp": 1492457001111, "sample_id": 7}]
```

4) Pobranie wyników z hosta źródłowego (receiver time)
```
GET <source_ip>:5000/measurement/icmp/receiver/<measurement_short_id>

Example response:
[{"timestamp": 1492457001151, "sample_id": 7}]
```

5) zakończenie pomiarów na hoście źródłowym
```
DELETE <source_ip>:5000/measurement/icmp/sender/<measurement_short_id>
```