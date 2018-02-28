FROM rabbitmq:3-management
USER root
RUN apt-get update && apt-get install python -y
COPY rabbitmqadmin /usr/local/bin/rabbitmqadmin
RUN chmod +x /usr/local/bin/rabbitmqadmin
COPY boot.sh .
RUN chmod +x boot.sh
CMD ./boot.sh

