#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import io
import urllib.request
import gzip
import argparse
import json
from datetime import datetime
from datetime import timedelta
import calendar
import pika
from conf import conf
from repository import repo_name

def rabbitMqInit():
	try:
		connection = pika.BlockingConnection(pika.ConnectionParameters(host=conf["rabbitMq"]["host"]))
		channel = connection.channel()
		return channel
	except Exception as e:
		print(e)

def definePath(path, date):
	tab = date.split("-")
	return path+'/'.join(tab[0:3])


def setCallURL(params):
	listDate = {}
	date = params.dateFormat

	if len(date.split("-")) == 2:
		return dayImporter(params)
	if len(date.split("-")) == 3:
		return hourImporter(date, params)
	return [{"filename":date+'.json' , "outPath": definePath(params.dest,params.dateFormat),
		"url": params.url+date+'.json.gz', "outPathFile": definePath(params.dest,params.dateFormat)+"/"+date+".json"}]


def hourImporter(date, params, callURL=[]):
	for hour in range(1,24):
		tmp = {}
		filename = date+'-'+str(hour)+'.json'
		tmp["outPath"] = definePath(params.dest,params.dateFormat)
		tmp["outPathFile"] = tmp["outPath"]+"/"+filename
		tmp["filename"]=filename
		tmp["url"]=params.url+filename+'.gz'
		callURL.append(tmp)
	return callURL

def dayImporter(params):
	callUrl= []
	splittedDate = params.dateFormat.split("-")
	lastDay = calendar.monthrange(int(splittedDate[0]),int(splittedDate[1]))[1]
	for day in range(1,lastDay):
		d = str(day).zfill(2)
		newDate = params.dateFormat+'-'+d
		hourImporter(newDate, params, callUrl)
	return callUrl


def init():
	params = []
	parser = argparse.ArgumentParser()
	parser.add_argument("--url", help="url source", default="http://data.githubarchive.org/")
	parser.add_argument("-df","--dateFormat", help="date format YYYY-MM-DD-HH", default= (datetime.now()+ timedelta(hours=-2)).strftime("%Y-%m-%d-%H"))
	parser.add_argument("-d","--dest", help="path where the file(s) store", default="/tmp/githubarchive/")
	args = parser.parse_args()
	params.append(setCallURL(args))
	return params

def pathBuilder(outFilePath):
	try:
		os.makedirs(outFilePath, exist_ok=True)
	except Exception as e:
		print(e)

def uploadFile(url):
	try:
		return urllib.request.urlopen(url)
	except Exception as e:
		print(e)

def decompressedFile(source):
	try:
		compressedFile = io.BytesIO()
		compressedFile.write(source.read())
		compressedFile.seek(0)
		#pathBuilder(dico["outPath"])
		return  gzip.GzipFile(fileobj=compressedFile, mode='rb')
	except Exception as e:
		print(e)

def prossessing(channel, uncompressedFile):
	line = str(uncompressedFile.readline(),'utf-8')
	while(line):
		jsonline = json.loads(line)
		if jsonline['repo']['name'] in repo_name:
			channel.basic_publish(exchange=conf["rabbitMq"]["exchange"],routing_key=conf["rabbitMq"]["routing_key"],body= line)
		line = str(uncompressedFile.readline(),'utf-8')

def importer(channel, workingList):
	for elt in workingList:
		for dico in elt:
			print("uploading file on "+dico['url'])
			try:
				compressedFile = uploadFile(dico["url"])
				uncompressedFile = decompressedFile(compressedFile)
				prossessing(channel, uncompressedFile)
			except Exception as e:
				print(e)
