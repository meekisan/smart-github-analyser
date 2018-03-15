FROM mongo:latest
USER root
RUN apt-get update && apt-get install apt-transport-https wget unzip -y
RUN apt-get install python3-pip -y
RUN pip3 install mongo-connector
RUN pip3 install neo4j-doc-manager
COPY ./datastorage/ /tmp/.
RUN mkdir -p /data/dbRsProjet
RUN chown mongodb:mongodb /data/dbRsProjet
