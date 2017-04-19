
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
from conda._vendor.auxlib.collection import frozendict


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
    if 'type' in kwargs:
        if kwargs['type'] == 'bool':
            results = execute_pylastic_boolean_search(input_string)
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

def filter_results(result_list):
    '''
    @summary: remove duplicates, and return only the 
    DatasetName, DatasetDescription, DatasetURL,
    '''
    filtered_results_set = set()
    for single_result in result_list:
        try:
            single_filtered_result = []
            single_filtered_result.append(single_result['datasetName'])
            single_filtered_result.append(single_result['datasetDescription'])
            single_filtered_result.append(single_result['datasetDistribution'])
            single_filtered_result.append( single_result.meta.score)            
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
    
    
    
    

#===============================================================================
# 
#===============================================================================
print("END of Pylastic Interface initialization, can now use functions")
