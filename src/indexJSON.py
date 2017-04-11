import csv
import json
import os
import requests
from elasticsearch import Elasticsearch
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Date, Nested, Boolean, analyzer, InnerObjectWrapper, Completion, Keyword, Text

es = Elasticsearch(timeout=300)
dataFolder = '../data/'

for dirname in os.listdir(dataFolder):
    for filename in os.listdir(os.path.join(dataFolder, dirname)):
        if filename.endswith('.json') and filename != 'meta.json':
            filepath =  os.path.join(dataFolder, dirname, filename)
            print('indexing: ' + filepath)
            jsonfile = open(filepath, 'r')
            data = json.load(jsonfile)
            res = es.index(index="baseindex", doc_type='basetype', body=data)
            print(res['created'])
            

