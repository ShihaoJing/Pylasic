# import httplib
# import csv2es
# import pyelasticsearch
# import elasticsearch
# from elasticsearch import Elasticsearch
# from elasticsearch_dsl.connections import connections
# from elasticsearch_dsl import Search, Q


import Pylastic_Interface as searcher
from nltk.draw.cfg import CFGEditor
  

#fucntion that parses the query
def parseQuery(query):
    searchType = None
    #first check the number of @ symbols in the query
    fields = query.split("@")
    #keywords = ["lte","gte","lt","gt"]
    #print(fields)
    bool_count = 0;
    range_count = 0;
    if len(fields) > 1:
        #bool_count = 0
        #range_count = 0
        #type of search can either be multi_range or mixed
        for field in fields:
            #print(field)
            #b = 0
            #r = 0
            input = field.split("#")
            fieldname = input[0]
            arguments = input[1].replace("[","").replace("]","")
            args = arguments.split(",")
            #print(args)
            for arg in args:
                print(k)
                print(arg)
                arg = arg.strip(" ")
                #print(arg)
                argfields = arg.split(":")
                #print(argfields)
                if len(argfields) == 1:
                    #boolean search
                    bool_count = bool_count + 1
                elif len(argfields) == 2:
                    #range search
                    range_count = range_count + 1 #this is not the case. Test to see if the name is the argument is valid
                    #TODO: Check to see if the arguments are valid
                else:
                    #this is an error
                    print("error")
        if(bool_count != 0 and range_count != 0):
            searchType = "mixed"
        elif(bool_count != 0 and range_count == 0):
            searchType = "bool"
        elif(bool_count == 0 and range_count != 0):
            searchType = "multi_range"
    else:
        #type of search can either be single rangle of bool
        #it will be bool if there is no detection of any of the keywords
        inputValues = query.split("#")
        fieldname = inputValues[0]
        arguments = inputValues[1].replace("[", "").replace("]", "")
        args = arguments.strip(" ").split(",")
        for arg in args:
            argfields = arg.split(":")
            if len(argfields) == 1:
                #searchType = "bool"
                bool_count = bool_count + 1
            elif len(argfields) == 2:
                #searchType = "single_range"
                range_count = range_count + 1
            else:
                print(error)
        if bool_count != 0 and range_count != 0:
            print("invalid syntax")
        elif bool_count != 0:
            searchType = 'bool'
        elif range_count != 0:
            searchType = 'single_range'
        else:
            print("It shouldn't have to come to this")
    #print(bool_count)
    #print(range_count)
    print(searchType)
    result = []
    result.append("data/%s"%(query))
    result.append(searchType)
    return result


#results = searcher.execute_pylastic_search("University of Arizona", type = 'bool')

# results = searcher.execute_pylastic_search("data/STNAM/ARIZONA", type = 'bool')
results = []
query = "@SAT_AVG#[gte:1000, lte:1200]"

query = query.strip(" ")
if(query[0] == '@'):
    inputString = parseQuery(query[1:])
    print(inputString)
    results = searcher.execute_pylastic_search(inputString[0], type = inputString[1])
else:
    results = searcher.execute_pylastic_search(query, type = 'bool')

#results = searcher.execute_pylastic_search(inputString, type = 'single_range')
  
if len(results) > 0:
    end_index = 3
    if len(results) <end_index:
        end_index = len(results)
    for r in results[:end_index]:
        print r
        
    for res in results:
        print res['score']
        


#===============================================================================
# 
#===============================================================================
# es = Elasticsearch(timeout=300)
# es.indices.delete(index = "_all")
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