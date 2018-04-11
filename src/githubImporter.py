import os
import io
from urllib.request import Request, urlopen
import gzip
import json
from datetime import datetime
from datetime import timedelta
from repository import repo_name
from logger.logger import logger
from conf import conf
import calendar


class GithubImporter:

    def __init__(self, url, dateFormat, dest):
        self.params = []
        self.callURL = []
        self.url = url
        self.dateFormat = dateFormat
        self.dest = dest
        self.params.append(self.setCallURL())

    def setBroker(self, broker):
        self.broker = broker

    def pathBuilder(self, outFilePath):
        try:
            os.makedirs(outFilePath, exist_ok=True)
        except OSError as err:
            logger.error(err)

    def uploadFile(self, url):
        try:
            self.sourceUrl =  urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'}))
        except IOError as err:
            logger.error(err)

    def decompressedFile(self):
        try:
            compressedFile = io.BytesIO()
            compressedFile.write(self.sourceUrl.read())
            compressedFile.seek(0)
            self.uncompressedFile = gzip.GzipFile(fileobj=compressedFile, mode='rb')
        except BlockingIOError as err:
            logger.error(err, err.args)

    def prossessing(self):
        line = str(self.uncompressedFile.readline(),'utf-8')
        while(line):
            jsonline = json.loads(line)
            if jsonline['repo']['name'] in repo_name:
                try:
                    self.broker.publish(line)
                except Exception as err:
                    logger.error(err)
            line = str(self.uncompressedFile.readline(),'utf-8')

    def work(self):
        for elt in self.callURL:
            try:
                self.uploadFile(elt["url"])
                self.decompressedFile()
                self.prossessing()
            except Exception as err:
                self.broker.close()
                logger.error(err)
        self.broker.close()

    def setCallURL(self):
        listDate = {}
        sizeDate = len(self.dateFormat.split("-"))
        if sizeDate == 2:
            self.dayImporter()
        elif sizeDate == 3:
            self.hourImporter()
        else:
            self.callURL = [{"filename":self.dateFormat+'.json', "url": self.url+self.dateFormat+'.json.gz'}]


    def hourImporter(self):
        for hour in range(1,24):
            tmp = {}
            filename = self.dateFormat+'-'+str(hour)+'.json'
            tmp["filename"]=filename
            tmp["url"]=self.url+filename+'.gz'
            self.callURL.append(tmp)

    def dayImporter(self):
        splittedDate = self.dateFormat.split("-")
        lastDay = calendar.monthrange(int(splittedDate[0]),int(splittedDate[1]))[1]
        for day in range(1,lastDay):
            d = str(day).zfill(2)
            newDate = self.dateFormat+'-'+d
            self.hourImporter(newDate)
