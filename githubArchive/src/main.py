#!/usr/bin/python3
from githubImporter import GithubImporter
from broker.rabbitMq import RabbitMq
from logger.logger import logger
import argparse
from datetime import datetime
from datetime import timedelta
from conf import conf


def checkParams():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="url source", default="http://data.githubarchive.org/")
    parser.add_argument("-df","--dateFormat", help="date format YYYY-MM-DD-HH", default= (datetime.now()+ timedelta(hours=-2)).strftime("%Y-%m-%d-%H"))
    parser.add_argument("-d","--dest", help="path where the file(s) store when it is not possible to publish messages", default="/tmp/githubarchive/")
    return parser.parse_args()


def main():
    logger.info("Run githubImporter")
    args = checkParams()
    importer = GithubImporter(args.url, args.dateFormat, args.dest)
    importer.setStrategy(RabbitMq(conf["rabbitMq"]["host"]))
    importer.setCallURL()
    importer.work()
    logger.info("End githubImporter")
if __name__ == "__main__":
    main()
