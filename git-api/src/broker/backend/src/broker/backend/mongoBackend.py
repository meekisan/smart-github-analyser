from .abstractBackend import AbstractBackend
from logger.logger import logger

import sys
import pymongo

class MongoBackend(AbstractBackend):
    def __init__(self, conf):
        self.host = conf['host']
        self.port = int(conf['port'])
        self.dbName = conf['db']
        self.collectionName = conf['collection']
        self.client = None
        self.db = None
        self.collection = None
        self.connect()

    def connect(self):
        try:
            self.client = pymongo.MongoClient(self.host,self.port)
            self.db = self.client[self.dbName]
            self.collection = self.db[self.collectionName]
        except Exception  as err:
            logger.error(err, err.args)
            sys.exit()

    def insert_one(self, data):
        print(data)
        try:
            self.collection.insert_one(data)
        except Exception as err:
            logger.error(err, err.args)
            sys.exit()

    def close(self):
        self.client.close()
