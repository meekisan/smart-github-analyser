FROM ubuntu
USER root
COPY ./src /data
WORKDIR /data
RUN chmod +x /data/main.py
RUN apt-get update && apt-get install cron && apt-get install python3-pip -y
RUN pip3 install pika pymongo
ADD ./githubArchive/crontab /etc/cron.d/githubImporter
RUN chmod 0644 /etc/cron.d/githubImporter
RUN touch /var/log/cron.log
CMD cron && tail -f /var/log/cron.log
