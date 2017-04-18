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
# each dataset folder has a meta.json file, which contains some meta data
metaJSON = json.load(open(os.path.join(dataFolder, 'meta.json')))
for dirpath, dirnames, filenames in os.walk(dataFolder):
    for filename in filesnames:
        if filename.endswith('.csv'):
            filepath =  os.path.join(dataFolder, filename)
            print('indexing: ' + filepath)
            # read csv file
            dataset = csv.DictReader(open(filepath, 'r'))
            # convert csv file to list of dictionaries
            dataList = list(dataset)
            # list of all attributes (column names)
            attrList = list(dataList[0].keys())
            # cut into 30 slices
            dataslices = slice_list(dataList, 30)
            for datagroup in dataslices:
                data = {'data': datagroup}
                data['datasetName'] = metaJSON['title']
                data['datasetDescription'] = metaJSON['description']
                data['datasetDistribution'] = metaJSON['distribution']
                data['keyword'] = metaJSON['keyword']
                data['filename'] = filename
                data['attrList'] = attrList
                # index name can be the name of dataset
                # doc_type name doesn't matter.
                res = es.index(index="testIndex", doc_type='basetype', body=data)
                print(res['created'])
