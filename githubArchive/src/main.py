#!/usr/bin/python3
import githubDataSetImporter

def main():
    channel = githubDataSetImporter.rabbitMqInit()
    workingList = githubDataSetImporter.init()
    githubDataSetImporter.importer(channel, workingList)

if __name__ == "__main__":
    main()
