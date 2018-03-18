#!/usr/bin/env python3
from broker.backend.elasticBackend import ElasticBackend
from broker.rabbitMq import RabbitMq
from logger.logger import logger

import argparse
from conf import conf


def checkParams():
    parser = argparse.ArgumentParser()
    parser.add_argument("-h","--host", help="broker host", default="rabbitmq")
    parser.add_argument("-p","--port", help="broker port", default= 16562)
    parser.add_argument("-q","--queue", help="consuming queue", default="test")
    return parser.parse_args()


def main():
    logger.info("Run consumer")
    broker = RabbitMq(conf["broker"]["search"])
    broker.setBackend(ElasticBackend(conf["elasticBackend"]))
    broker.consume()
    logger.info("End consumer")

if __name__ == "__main__":
    main()
