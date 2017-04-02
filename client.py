from datetime import datetime
from elasticsearch import Elasticsearch
import json
es = Elasticsearch()

dataset1 = {
    'title': '1st dataset',
    'text': "I'm the first data set",
    'timestamp': datetime.now(),
}

dataset2 = {
    'title': '2nd dataset',
    'text': "I'm the second data set",
    'timestamp': datetime.now(),
}

dataset3 = {
    'title': '3rd dataset',
    'text': "I'm the third data set",
    'timestamp': datetime.now(),
}

res = es.index(index="all", doc_type='test', id=1, body=dataset1)
print(res)

res = es.index(index="all", doc_type='test', id=2, body=dataset2)
print(res)

res = es.index(index="all", doc_type='test', id=3, body=dataset3)
print(res)

es.indices.refresh(index="test-index")

res = es.search(index="all", body={"query": {"match_all": {}}})

source = []
print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
    source.append(hit["_source"])

print(json.dumps(source))