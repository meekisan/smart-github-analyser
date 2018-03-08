FROM rabbitmq:3-management
USER root
RUN apt-get update && apt-get install python -y
COPY rabbitmqadmin /usr/local/bin/rabbitmqadmin
RUN chmod +x /usr/local/bin/rabbitmqadmin
RUN mkdir -p /data
COPY boot.sh /data
RUN chmod +x /data/boot.sh
#CMD ./data/boot.sh
