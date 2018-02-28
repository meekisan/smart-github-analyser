FROM ubuntu
USER root
COPY src /data
WORKDIR /data 
RUN apt-get update && apt-get install python3-pip -y
RUN pip3 install pika
CMD sleep infinity
