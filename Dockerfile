FROM ubuntu:16.04

RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
RUN echo "deb http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.2 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-3.2.list

RUN apt-get update -y && apt-get install -y python-pip mongodb-org net-tools
RUN pip install --upgrade pip
RUN pip install scapy netifaces flask pymongo bitstring

RUN mkdir -p /data/db
ADD Netprobe.tar.gz /opt

ENV NET_INTERFACE eth0
CMD sh -c "(mongod --port 50000 &) && (sleep 1 ; python /opt/netprobe/Netprobe.py $NET_INTERFACE)"
