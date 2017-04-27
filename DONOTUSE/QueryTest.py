from elasticsearch import Elasticsearch

es = Elasticsearch(timeout=300)

body = {
  "_source": ["datasetName"],
  "query": {
    "nested": {
      "path": "data",
      "query": {
        "bool": {
          "must": [
            { "match": { "data.IND_INC_PCT_H1": "PrivacySuppressed"  }}
          ]
        }
      }
    }
  }
}

body2 = {
  "_source": ["datasetName", "datasetDistribution.downloadURL", "datasetDescription"],
  "query": {"match": {"datasetDescription": "school"}}
}

res = es.search(body=body2)
print(res['hits']['total'])
print(res['hits']['hits'][0]["_source"])