FROM ubuntu:16.04

RUN apt-get update -y && apt-get install -y --no-install-recommends software-properties-common

RUN \
  echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | debconf-set-selections && \
  add-apt-repository -y ppa:webupd8team/java && \
  apt-get update && \
  apt-get install -y oracle-java8-installer && \
  rm -rf /var/lib/apt/lists/* && \
  rm -rf /var/cache/oracle-jdk8-installer

RUN apt-get update -y && apt-get install -y libpcap0.8 libpcap0.8-dev iputils-ping

RUN mkdir /opt/netprobe
ADD target/netprobe-1.0-SNAPSHOT-jar-with-dependencies.jar /opt/netprobe
ADD jnetpcap-1.3.0-1.ubuntu.x86_64.tgz /opt/netprobe

CMD java \
  -cp /opt/netprobe/jnetpcap-1.3.0/jnetpcap.jar:/opt/netprobe/netprobe-1.0-SNAPSHOT-jar-with-dependencies.jar \
  -Djava.library.path=/opt/netprobe/jnetpcap-1.3.0 \
  pl.edu.agh.tip.netprobe.Main

