from .abstractBackend import AbstractBackend
from logger.logger import logger
import requests
import time
import sys


class ElasticBackend(AbstractBackend):
    def __init__(self, conf):
        self.url = conf['url']
        self.connect();

    def connect(self):
        time.sleep(20)

    def insert_one(self, data):
        try:
            requests.post('http://search:9200/github/archives', json=data)
        except Exception as err:
            logger.error(err, err.args)
            sys.exit()

    def close(self):
        pass
