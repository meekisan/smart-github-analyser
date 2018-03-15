from broker.rabbitMq import RabbitMq
from logger.logger import logger
from conf import conf
from flask import Flask
from flask import request
import requests
import json

app = Flask(__name__)

@app.route('/commit', methods=['POST'])
def commit():
    receivedData = request.get_data().decode('utf-8')
    receivedData = receivedData.replace("\r\n","\n")
    broker = RabbitMq(conf['broker']['simulator'])
    broker.publish(receivedData)
    return 'OK'
