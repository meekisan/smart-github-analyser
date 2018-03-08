FROM mongo
USER root
RUN apt-get update && apt-get install apt-transport-https nano wget unzip -y
RUN apt-get install python3-pip -y
RUN pip3 install mongo-connector
RUN mkdir /data/dbRsProjet
RUN mongod --replSet rsProjet --bind_ip_all --dbpath /data/dbRsProjet > /dev/null&
CMD sleep infinity
