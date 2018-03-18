import unittest
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
import githubDataSetImporter

class test_importer(unittest.TestCase):

    def test_repo_name(self):
        compressedFile = open("./tests/2018-03-01-13.json.gz","rb")
        uncompressedFile = githubDataSetImporter.decompressedFile(compressedFile)
        compressedFile.close()
        line = json.loads(str(uncompressedFile.readline(),'utf-8'))
        self.assertEqual(line['repo']['name'], "sundarbee/NewLibraryExample")


if __name__ == '__main__':
    unittest.main()
