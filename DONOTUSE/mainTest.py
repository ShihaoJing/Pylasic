
# import httplib
# import csv2es
# import pyelasticsearch
# import elasticsearch
# from elasticsearch import Elasticsearch
# from elasticsearch_dsl.connections import connections
# from elasticsearch_dsl import Search, Q

import Pylastic_Interface as searcher


results = searcher.execute_pylastic_search("San Francisco", type = 'bool')

if len(results) > 3:
    for r in results[:3]:
        print r['datasetName']
        print r['score']

#------------------------OLD CODE----------------------------------- 
# 
# connections.create_connection(hosts=['localhost:9200'], timeout=20)
# 
# 
# 
# # conn = httplib.HTTPConnection("localhost:9200")
# # conn.request("GET","/")
# # res = conn.getresponse()
# # print res.status, res.reason
# # print res.read()
# 
# '''
# NEXT:
# import some csv files using 
# https://pypi.python.org/pypi/csv2es
# from the data folder
# '''
# 
# dataFolder = "../data/"
# 
# 
# #===========================================================================
# #   THIS IS ONE WAY TO INDEX. there seems to be a limit of 1k fields per index. Which is generous,
# #    but surprisingly one csv file had more than that ??
# #   also is this limit a lucene/es limit, or the client limit. Does the "official client improve this" 
# #===========================================================================
# #csv2es --index-name potatoes --doc-type potato --import-file potatoes.cs
# 
# 
# 
# # def funFunction(**kwargs):
# #     for a in kwargs:
# #         print (a,kwargs[a])
# # funFunction(a="A", b="B")        
# 
# '''
# pip-install csv2es
# pip-install pyelasticsearch
# change the file name to your csv file
# '''
# 
# # es_client = pyelasticsearch.ElasticSearch('http://localhost:9200/')
# # myDocuments = csv2es.documents_from_file(es_client, "./test_small.csv", ",", quiet = False)
# # csv2es.perform_bulk_index(host = 'http://localhost:9200/'
# #                           , index_name = "baseindex",
# #                            doc_type = "basedoctype",
# #                            doc_fetch = myDocuments,
# #                            docs_per_chunk = 5000,
# #                            bytes_per_chunk = 100000,
# #                            parallel = 1)
# 
# #===============================================================================
# # 
# #===============================================================================
# 
# #query and filter search testing
# #-------------------------------------------------------------------------------------
# #------------------------------------------------------------------------------
# 
# s = Search()
# q = Q('bool',must=[Q('match', _all='San Francisco')])
# 
# s = s.query(q)
# print(s.to_dict())
# 
# response = s.execute()
# for hit in response[1:10]:
#     print(hit.INSTNM)




print("END of elastic search test script")
