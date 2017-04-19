import json, csv, os
from elasticsearch import Elasticsearch

es = Elasticsearch(timeout=300)

def slice_list(input, size=30):
    input_size = len(input)
    slice_size = input_size / size
    remain = input_size % size
    result = []
    iterator = iter(input)
    for i in range(size):
        result.append([])
        for j in range(slice_size):
            result[i].append(iterator.next())
        if remain:
            result[i].append(iterator.next())
            remain -= 1
    return result

#dataFolder = '../data/College Scorecard/'
dataFolder = '../data'

def createIndex(indexname):
    index_settings = {
        "settings": {
            "index.mapping.total_fields.limit": 5000
        },
        "mappings": {
            "basetype": {
                "_all": { "enabled": True  }, 
            "properties": { 
                "data" : {"type": "nested"}
              }
            }
        }
    }
    es.indices.create(index=indexname, body=index_settings)

def doIndex(indexname, input_data): 
    res = es.index(index=indexname, doc_type='basetype', body=input_data)
    return res['created']

dataset_count = 0
# each dataset folder has a meta.json file, which contains some meta data
for dirname in os.listdir(dataFolder):
    metaJsonFilePath = os.path.join(dataFolder, dirname, 'meta.json')
    if os.path.exists(metaJsonFilePath):
        metaJSON = json.load(open(metaJsonFilePath))
        print("indexing dataset %s" % dirname)
        indexname = "dataset" + str(dataset_count)
        createIndex(indexname)
        dataset_count = dataset_count + 1
        for filename in os.listdir(os.path.join(dataFolder, dirname)):
            if filename.endswith('.csv'):
                filepath =  os.path.join(dataFolder, dirname, filename)
                print('indexing: ' + filepath)
                # read csv file
                dataset = csv.DictReader(open(filepath, 'r'))
                # convert csv file to list of dictionaries
                dataList = list(dataset)
                # list of all attributes (column names)
                attrList = list(dataList[0].keys())
                # cut into slices, default is 30 slices per file
                dataslices = slice_list(dataList)
                for index, datagroup in enumerate(dataslices):
                    input_data = {'data': datagroup}
                    input_data['datasetName'] = metaJSON['title']
                    input_data['datasetDescription'] = metaJSON['description']
                    input_data['datasetDistribution'] = metaJSON['distribution']
                    input_data['keyword'] = metaJSON['keyword']
                    input_data['filename'] = filename
                    input_data['attrList'] = attrList
                    # index name can be the name of dataset
                    # doc_type name doesn't matter.
                    print('indexing slices %s' % str(index))
                    print(doIndex(indexname, input_data))


