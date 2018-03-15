FROM ubuntu
USER root
RUN apt-get update && apt-get install python3-pip -y
RUN pip3 install Flask
RUN pip3 install pika
RUN pip3 install requests
RUN pip3 install pymongo
ENTRYPOINT []
WORKDIR /data
CMD flask run --port 80 --host 0.0.0.0
