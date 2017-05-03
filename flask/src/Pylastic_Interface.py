
'''
@summary: This script contains the functions that allow the Pylastic flask web server
to search and get results from the Elastic Search instance/node that is running
'''



import httplib

import csv2es
from elasticsearch import Elasticsearch
import elasticsearch
import pyelasticsearch


from elasticsearch_dsl import Search, Q
from elasticsearch_dsl.connections import connections


connections.create_connection(hosts=['localhost:9200'], timeout=20)
#===============================================================================
# 
#===============================================================================

def execute_pylastic_search(input_string, **kwargs):
    '''
    @param input_string: the user's query string
    @param **kwargs: Key word arguments that define the query. eg: type = 'bool' will run a boolean query
    @return: an ordered list of results. [{doc1 info}, {doc2 info},....]
            each doc info contains the "name", "URL", "snippet","score". snippet contains the matching parts of the doc.
    '''
    results = []
    parts = input_string.split(",")
    for single_part in parts: #this splitting allows many searches , 
                            #BUT currently all the results are put in one big container       
        if 'type' in kwargs:
            if kwargs['type'] == 'bool':
                a = execute_pylastic_boolean_search(single_part)
                results = results + a.hits.hits
            elif kwargs['type'] == 'single_range':
                a = execute_pylastic_singleRange_search(single_part)
                results = results + a.hits.hits 
            elif kwargs['type'] == 'datafield':
                a = execute_pylastic_dataFields_search(single_part)
                results = results + a.hits.hits    
    if len(results) >0 :
        results = filter_results(results)
    return results
#END FUNCTION
#===============================================================================
# 
#===============================================================================
def execute_pylastic_boolean_search(input_string):
    '''
    @summary: execute a boolean search with the input string on all fields
    @return: an ordered list of results. [{doc1 info}, {doc2 info},....]
        each doc info contains the "name", "URL", "snippet","score". snippet contains the matching parts of the doc.
    '''
    s = Search()      
    path_parts = input_string.split("/")
    q = None
    if len(path_parts) > 1:
        path_to_search = ".".join(path_parts[:-2])
        area_to_search = ".".join(path_parts[:-1]) #+ ["_all"])
        q =Q("nested", path = path_to_search ,query = Q('bool',
            must=[Q('match',**{area_to_search:path_parts[-1]})]))                
        
    else:                
        q = Q('bool',must=[Q('match', _all=input_string)])            
    s = s.query(q)
    print("running boolean query \n", s.to_dict())    
    response = s.execute()
    return response
#===============================================================================
# 
#===============================================================================
def execute_pylastic_dataFields_search(inputString,**kwargs):
    '''
    @param kwards: A dictionary containing the field name  
    @summary: will go through the entries in the data fields and find matching documents
    kwargs contain the field names as keys, and the search term(s) as values. Value can be a single
    string, in which case a 'term' search will be done. It can also be a list, in which case
    a "termS" search will be done. 
    @return: an ordered list of results. [{doc1 info}, {doc2 info},....]
        each doc info contains the "name", "URL", "snippet","score". snippet contains the matching parts of the doc.
    
    '''
    #to be done
    s = Search();
    datafield_parts = inputString.split('@')
    #the first element of datafield should be an empty string. We want to remove that
    datafield_parts = datafield_parts[1:]
    print(datafield_parts)
    for field in datafield_parts:
        field = field.split(':')
        attribute = field[0]
        value = field[1]

        #attribute,value = field.split(',')
        #print(attribute)
        #print(value)
    pass
#===============================================================================
# 
#===============================================================================
def execute_pylastic_NON_dataFields_search(inputString,):
    '''    
    @summary: perform a search on all fields in a document OTHER THAN the "data" field
    so it will go through metadata, URL etc.
    @return: an ordered list of results. [{doc1 info}, {doc2 info},....]
        each doc info contains the "name", "URL", "snippet","score". snippet contains the matching parts of the doc.     
    '''
    #to be done
    pass

#===============================================================================
# 
#===============================================================================

def getURLlistFromDistribution(distributionInfo_listOfDict):
    '''
    '''
    return_list_urls = []
    
    for eachContainer in distributionInfo_listOfDict:
        if 'accessURL' in eachContainer.keys():
            return_list_urls.append(eachContainer['accessURL'])
        elif 'downloadURL' in eachContainer.keys():
            return_list_urls.append(eachContainer['downloadURL'])
        else:
            allValues = list(eachContainer.values())
            for eachValue in allValues:
                if eachValue[1].startswith("http") or \
                        eachValue[1].startswith("www"):
                    return_list_urls.append(eachValue[1])
                #end if
            #end for
        #end else
    #end for
    return return_list_urls
                             

#===============================================================================
# 
#===============================================================================

def filter_results(result_list):
    '''
    @summary: remove duplicates, and return only the 
    DatasetName, DatasetDescription, DatasetURL,
    '''
    filtered_results_set = set()
    for single_result in result_list:
        try:
            single_filtered_result = []
            single_filtered_result.append(single_result['_source']['datasetName'])
            single_filtered_result.append(single_result['_source']['datasetDescription'])
            single_filtered_result.append(
                tuple(getURLlistFromDistribution(single_result['_source']['datasetDistribution'])))
            single_filtered_result.append( single_result['_score'])            
            filtered_results_set.add(tuple(single_filtered_result))
        except:
            print("Unexpected error, unable to find the expected fields in the doc")
    #end for loop
    temp = list(filtered_results_set)
    temp.sort(key = lambda x:x[3], reverse = True)
    #now convert it back into a dict
    return_results_list = []
    for single_result in temp:
        dict_form = {}
        dict_form['datasetName'] = single_result[0]
        dict_form['datasetDescription'] = single_result[1]
        dict_form['datasetDistribution'] = single_result[2]
        dict_form['score'] = single_result[3]
        return_results_list.append(dict_form)
    return return_results_list    
    
    
    
#===========================================================================
# 
#===========================================================================

def execute_pylastic_singleRange_search(input_string):
    '''
    @note: See https://github.com/elastic/elasticsearch-dsl-py/issues/40 for range queries in dsl
    @param inputString: expect the field name and the range parameters in  
    the format Age gte:10 lte:20
    @summary: Does the following type of search for a single field
        "query": {
        "range" : {
            "age" : {
                "gte" : 10,
                "lte" : 20,
                "boost" : 2.0
            }
    '''
    
    parts = input_string.split()
    if len(parts) == 1 or ":" not in input_string:
        raise(Exception,\
            "Range was not specified properly when calling execute_pylastic_singleRange_search")
    #fill the range conditions into range_param_dict         
    range_param_dict = {}
    for i in range(1,len(parts)):
        rangeParts = parts[i].split(":")
        range_param_dict[rangeParts[0]] = rangeParts[1]    
    s = Search()    
    path_parts = parts[0].split("/")
    q = None
    #check if this is a nested search, i.e. the path has "/"
    if len(path_parts) > 1:
        path_to_search = ".".join(path_parts[:-1])
        area_to_search = ".".join(path_parts) #+ ["_all"])
        a = area_to_search
        range_search_dict = {a:range_param_dict}
        q =Q("nested", path = path_to_search ,query = Q('range',**range_search_dict))                
        
    else:#it is not a nested search
        range_search_dict = {a:range_param_dict}                
        q = Q('range',**range_search_dict)     
 
    s = s.query(q)
    print("running range query on single field \n", s.to_dict())    
    response = s.execute()
    return response
    
    

#===============================================================================
# 
#===============================================================================
print("END of Pylastic Interface initialization, can now use functions")
