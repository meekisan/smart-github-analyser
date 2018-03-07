import pika
import json
from bson import json_util
from .abstractBroker import AbstractBroker
from logger.logger import logger

class RabbitMq(AbstractBroker):

    def __init__(self, conf):
        self.host = conf['host']
        self.port = conf['port']
        self.exchange = conf['exchange']
        self.routing_key = conf['routing_key']
        self.queue = conf['queue']
        self.backend = None
        self.connect()

    def connect(self):
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
            self.channel = self.connection.channel()
        except Exception as err:
            logger.error(err, err.args)

    def setBackend(self, backend):
        self.backend = backend

    def publish(self, data):
        try:
            self.channel.basic_publish(exchange=self.exchange,routing_key=self.routing_key,body=data)
        except KeyboardInterrupt as err:
            logger.error(err, err.args)

    def callback(self, channel, method, property, body):
        try:
            if self.backend:
                self.backend.insert_one(json.loads(str(body,'utf-8')))
        except Exception as err:
            logger.error(err, err.args)

    def consume(self):
        try:
            self.channel.basic_consume(self.callback, self.queue, no_ack=True)
            self.channel.start_consuming()
        except (Exception, KeyboardInterrupt) as err:
            self.channel.stop_consuming()
            self.close()
            logger.error(err, err.args)

    def close(self):
        self.connection.close()
