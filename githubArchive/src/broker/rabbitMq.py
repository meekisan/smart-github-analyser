import pika
from .abstractBroker import AbstractBroker

class RabbitMq(AbstractBroker):

    def __init__(self, host="localhost", port=5672):
        self.host = host
        self.port = port
        self.connect()

    def connect(self):
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
            self.channel = self.connection.channel()
        except Exception as e:
            print(e)

    def publish(self, exchange, routing_key, data):
        try:
            self.channel.basic_publish(exchange=exchange,routing_key=routing_key,body=data)
        except Exception as e:
            print(e)

    def callback(self, channel, method, property, body):
        
        print(" [x] %r" % body)



    def consume(self, queue):
        print("RabbitMq consumer")
        self.channel.basic_consume(self.callback, queue, no_ack=True)
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()

    def close(self):
        self.connect.close()
