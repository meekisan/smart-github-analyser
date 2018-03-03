from rabbitMq import RabbitMq

broker = RabbitMq()
broker.connect()
broker.publish()
broker.consumer()
