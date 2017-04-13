# netprobe

```
sudo docker build -t netprobe .
sudo docker run --network="host" -e NET_INTERFACE=<your_interface> netprobe
```

<!--`sudo pip install scapy==2.2.0-dev`-->