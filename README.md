# netprobe
```
provide ${project.basedir}/lib/jnetpcap-1.3.0/jnetpcap.jar
mvn compile assembly:single
sudo docker build -t netprobe .
sudo docker run netprobe
```
