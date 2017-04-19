import csv
import json
import os
import requests


def download_file(url, filepath):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(os.path.join(filepath, local_filename), 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    return local_filename

dataFolder = '../data/'
for dirname in os.listdir(dataFolder):
    for filename in os.listdir(os.path.join(dataFolder, dirname)):
        if filename == 'meta.json':
            filepath =  os.path.join(dataFolder, dirname)
            print(filepath)
            metaJson = open(os.path.join(filepath, filename))
            metaJson = json.load(metaJson)
            for item in metaJson['distribution']:
                if 'format' in item and item['format'] == 'CSV':
                    jsonfile = {}
                    datasetName = ''
                    if 'downloadURL' in item:
                        jsonfile['downloadURL'] = item['downloadURL']
                        datasetName = item['downloadURL'].split('/')[-1]
                    if 'accessURL' in item:
                        jsonfile['downloadURL'] = item['accessURL']
                        datasetName = item['accessURL'].split('/')[-1]

                    jsonfile_name = os.path.join(filepath, datasetName.split('.')[0] + '.json')
                    try:
                        dataset = open(os.path.join(filepath, datasetName))
                    except IOError:
                        print "Could not open file! Start download"
                        download_file(jsonfile['downloadURL'], filepath)
                        dataset = open(os.path.join(filepath, datasetName))
                    reader = csv.DictReader(dataset)
                    rows = list(reader)

                    jsonfile['title'] = metaJson['title']
                    jsonfile['description'] = metaJson['description']
                    jsonfile['format'] = item['format']
                    jsonfile['keyword'] = metaJson['keyword']
                    jsonfile['data'] = json.dumps(rows)

                    with open(jsonfile_name, 'w') as f:
                        json.dump(jsonfile, f)

