import os
import io
import urllib.request
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

    def setStrategy(self, strategy):
        self.strategy = strategy

    def pathBuilder(self, outFilePath):
        try:
            os.makedirs(outFilePath, exist_ok=True)
        except Exception as e:
            print(e)

    def uploadFile(self, url):
        try:
            self.sourceUrl =  urllib.request.urlopen(url)
        except Exception as e:
            print(e)

    def decompressedFile(self):
        try:
            compressedFile = io.BytesIO()
            compressedFile.write(self.sourceUrl.read())
            compressedFile.seek(0)
            self.uncompressedFile = gzip.GzipFile(fileobj=compressedFile, mode='rb')
        except Exception as e:
            loggger.error(e)
            print(e)

    def prossessing(self):
        line = str(self.uncompressedFile.readline(),'utf-8')
        while(line):
            jsonline = json.loads(line)
            if jsonline['repo']['name'] in repo_name:
                try:
                    self.strategy.publish(conf["rabbitMq"]["exchange"], conf["rabbitMq"]["routing_key"], line)
                except Exception as e:
                    loggger.error(e)
                    print(e)
            line = str(self.uncompressedFile.readline(),'utf-8')

    def work(self):
        for elt in self.callURL:
            try:
                self.uploadFile(elt["url"])
                self.decompressedFile()
                self.prossessing()
            except Exception as e:                
                loggger.error(e)
                print(e)

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
