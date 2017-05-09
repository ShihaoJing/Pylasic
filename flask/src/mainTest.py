# import httplib
# import csv2es
# import pyelasticsearch
# import elasticsearch
# from elasticsearch import Elasticsearch
# from elasticsearch_dsl.connections import connections
# from elasticsearch_dsl import Search, Q


import Pylastic_Interface as searcher
from nltk.draw.cfg import CFGEditor
  

helpMessage = "The \'@\' symbol starts each field search, and is followed by the field you want to search in \nThe \'#\' symbol starts the list of values that you expect to find in the field\nIf you expect a numeric field, the the upper and lower bound of values must be specified.\n To specify the bounds, the following conditions can be used\n a) gte - greater than or equal to\n b) lte - less than or equal to\n c) gt - greater than\n d) lt - less than\nLastly, sperate successive terms inside the \'[..]\' by a comma"

#fucntion that parses the query
def parseQuery(query):
    searchType = None
    keywords = ["lte","gte","lt","gt"]
    #first check the number of @ symbols in the query
    fields = query.split("@")
    #print(fields)
    bool_count = 0;
    range_count = 0;
    queryOperators = [] #this is the store the operators used in the query to test if it defines the proper boundaries
    if len(fields) > 1:
        #type of search can either be multi_range or mixed
        for field in fields:
            input = field.split("#")
            fieldname = input[0]
            arguments = input[1].replace("[","").replace("]","")
            args = arguments.strip(" ").split(",")
            #print(args)
            for arg in args:
                #print(arg)
                #arg = arg.strip(" ")
                #print(arg)
                argfields = arg.strip(" ").split(":")
                #print(argfields)
                if len(argfields) == 1:
                    #boolean search
                    bool_count = bool_count + 1
                elif len(argfields) == 2:
                    #range search
                    #check to see that there are two values for the range search
                    if len(args) != 2:
                        printError("A range query should have 2 arguments to set the bounds")
                    #Check to see if the operator is valid
                    valid = False
                    print(argfields[0])
                
                    for op in keywords:
                        if op == argfields[0]:
                            valid = True
                            queryOperators.append(op)
                            break
                    if not(valid):
                        printError("Unknown comparison operator")
                    #the second value should be a numeric value
                    if not(argfields[1].isdigit()):
                        printError("Range values must be numeric")
                    range_count = range_count + 1 #this is not the case. Test to see if the name is the argument is valid
                    #TODO: Check to see if the arguments are valid
                else:
                    #this is an error
                     printError("This is improper syntax")
            #check the operators used in the query to make sure that the bounds of the range search are properly defined
            if len(queryOperators) != 0: 
                if len(queryOperators) != 2: #shouldn't need this, but just to double check
                    printError("A range query should have 2 arguments to set the bounds") 
                if queryOperators[0] == queryOperators[1]:
                    printError("Cannot define the same bound twice")
                if queryOperators[0] == "lt" or queryOperators[0] == "lte":
                    if queryOperators[1] != "gte" and queryOperators[1] != "gt":
                        printError("Bounds of the range search are not properly defined")
                elif queryOperators[0] == "gt" or queryOperators[0] == "gte":
                    if queryOperators[1] != "lte" and queryOperators[1] != "lt":
                        printError("Bounds of the range search are not properly defined")
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
            argfields = arg.strip(" ").split(":")
            if len(argfields) == 1:
                #searchType = "bool"
                bool_count = bool_count + 1
            elif len(argfields) == 2:
                #check to see that there are two values for the range search
                if len(args) != 2:
                    printError("A range query should have 2 arguments to set the bounds")
                #Check to see if the operator is valid
                valid = False
                print(argfields[0])
                
                for op in keywords:
                    if op == argfields[0]:
                        valid = True
                        queryOperators.append(op)
                        break
                if not(valid):
                    printError("Unknown comparison operator")
                #the second value should be a numeric value
                if not(argfields[1].isdigit()):
                    printError("Range values must be numeric")
                range_count = range_count + 1
            else:
                printError("This is improper syntax")
        #check the operators used in the query to make sure that the bounds of the range search are properly defined
        if len(queryOperators) != 0:
            if len(queryOperators) != 2: #shouldn't need this, but just to double check
                printError("A range query should have 2 arguments to set the bounds") 
            if queryOperators[0] == queryOperators[1]:
                printError("Cannot define the same bound twice")
            if queryOperators[0] == "lt" or queryOperators[0] == "lte":
                if queryOperators[1] != "gte" and queryOperators[1] != "gt":
                    printError("Bounds of the range search are not properly defined")
            elif queryOperators[0] == "gt" or queryOperators[0] == "gte":
                if queryOperators[1] != "lte" and queryOperators[1] != "lt":
                    printError("Bounds of the range search are not properly defined")
        #determine the search type
        if bool_count != 0 and range_count != 0:
            printError("Field search cannot contain a range and a value")
        elif bool_count != 0:
            searchType = 'bool'
        elif range_count != 0:
            searchType = 'single_range'
        else:
            printError("It shouldn't have come to this")
    #print(bool_count)
    #print(range_count)
    print(searchType)
    if searchType == None:
        printError("Could not determin the type of search")
    result = []
    if searchType=='bool' or searchType=='single_range':
        result.append("data/%s"%(query))
    else:
        newQuery = query.replace("@","data/") #I am not sure if this is what we want to pass
        result.append("data/%s"%(newQuery))
    result.append(searchType)
    return result

def printError(message):
    print("ERROR: %s\n"%(message))
    print(helpMessage)
    quit()

#results = searcher.execute_pylastic_search("University of Arizona", type = 'bool')

# results = searcher.execute_pylastic_search("data/STNAM/ARIZONA", type = 'bool')
results = []
query = "@SAT_AVG#[gt:1000, lte:1200] @City#[New York, San Francisco]"

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