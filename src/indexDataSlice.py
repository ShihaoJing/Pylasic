import json, csv, os
from elasticsearch import Elasticsearch

es = Elasticsearch(timeout=300)

def slice_list(input, size):
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
dataFolder = '../data/Consolidated State Performance Report, 2009-10'

metaJSON = json.load(open(os.path.join(dataFolder, 'meta.json')))
for filename in os.listdir(dataFolder):
    if filename.endswith('.csv'):
        filepath =  os.path.join(dataFolder, filename)
        print('indexing: ' + filepath)
        dataset = csv.DictReader(open(filepath, 'r'))
        dataList = list(dataset)
        attrList = list(dataList[0].keys())
        dataslices = slice_list(dataList, 30)
        for datagroup in dataslices:
            data = {'data': datagroup}
            data['datasetName'] = metaJSON['title']
            data['datasetDescription'] = metaJSON['description']
            data['datasetDistribution'] = metaJSON['distribution']
            data['keyword'] = metaJSON['keyword']
            data['filename'] = filename
            data['attrList'] = attrList
            res = es.index(index="baseindex3", doc_type='basetype', body=data)
            print(res['created'])
