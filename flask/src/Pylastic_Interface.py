
'''
@summary: This script contains the functions that allow the Pylastic flask web server
to search and get results from the Elastic Search instance/node that is running
'''



import copy
import httplib

import csv2es
from elasticsearch import Elasticsearch
import elasticsearch
import pyelasticsearch

from elasticsearch_dsl import Search, Q
from elasticsearch_dsl.connections import connections
from bokeh.charts.builders.area_builder import Area
from contextlib import nested
from sympy.strategies.branch.core import condition


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
    parts = input_string.split("&&")#arbitrary separator between terms
    for single_part in parts: #this splitting allows many searches , 
                            #BUT currently all the results are put in one big container       
        if 'type' in kwargs:
            if kwargs['type'] == 'bool':
                a = execute_pylastic_boolean_search(single_part)
                results = results + a.hits.hits
            if kwargs['type'] == 'phrase':
                a = execute_pylastic_phrase_search(single_part)
                results = results + a.hits.hits                
            elif kwargs['type'] == 'single_range':
                raise(Exception,\
                      "use mixed search, multiple range and single range search is discontinued")                
            elif kwargs['type'] == 'multiple_range':
                raise(Exception,\
                      "use mixed search, multiple range and single range search is discontinued")
                a = execute_pylastic_multipleRange_search(single_part)
                results = results + a.hits.hits
            elif kwargs['type'] == 'mixed':
                a = execute_pylastic_mixed_search(single_part)
                results = results + a.hits.hits                
    if len(results) >0 :
        results = filter_results(results)
        add_additional_UI_info(results)
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
def execute_pylastic_phrase_search(input_string):
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
            must=[Q('match_phrase',**{area_to_search:path_parts[-1]})]))                
        
    else:                
        q = Q('bool',must=[Q('match_phrase', _all=input_string)])            
    s = s.query(q)
    print("running boolean query \n", s.to_dict())    
    response = s.execute()
    return response



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
    DatasetName, DatasetDescription, DatasetURL, Score, Keywords, and AttributeList
    '''
    filtered_results_set = set()    
    seen_results_set = set()
    for single_result in result_list:
        try:
            single_filtered_result = []
            single_filtered_result.append(single_result['_source']['datasetName'])
            single_filtered_result.append(single_result['_source']['datasetDescription'])
            single_filtered_result.append(
                tuple(getURLlistFromDistribution(single_result['_source']['datasetDistribution'])))
            if tuple(single_filtered_result) not in seen_results_set:
                seen_results_set.add(tuple(single_filtered_result))                                 
                single_filtered_result.append( single_result['_score'])
                single_filtered_result.append( tuple(single_result['_source']['keyword']))
                single_filtered_result.append( tuple(single_result['_source']['attrList']))             
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
        dict_form['keywords'] = single_result[3]
        dict_form['attrList'] = single_result[3]
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
    
    parts = input_string.split("#")
    if len(parts) == 1 or "[" not in input_string or  "]" not in input_string:
        raise(Exception,\
            "Range was not specified properly when calling execute_pylastic_singleRange_search")
        
    #fill the range conditions into range_param_dict             
    range_info_string = parts[1]
    range_info_string = range_info_string.replace("[","")
    range_info_string = range_info_string.replace("]","")
    constraints_parts = range_info_string.split(",")
    range_param_dict = {} 
    for i in range(0,len(constraints_parts)):
        constraints_parts[i] = constraints_parts[i].replace(" " , "")                
        rangeParts = constraints_parts[i].split(":")
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
    
#===========================================================================
# 
#===========================================================================

def execute_pylastic_multipleRange_search(input_string):
    '''
    
    @param inputString: expect multiple cases of the form @<field>#[range/values]@<field2>#values2]
    @summary: Does the following type of search which has many ranged fields
    can be nested too, but then all must be of the same nesting.
        "query": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                "created_at": {
                                    "gte": "2013-12-09T00:00:00.000Z"
                                }
                            }
                        },
                        {
                            "range": {
                                "happens_on": {
                                    "lte": "2013-12-16T00:00:00.000Z"
                                }
                            }
                        }
                    ]
                }
            }
    '''
    
    range_conditions_list = input_string.split("]")
    #remove the last one as it will be '' empty string
    range_conditions_list = range_conditions_list[:-1]
    if "[" not in input_string and "]" not in input_string :
        raise(Exception,\
            "Range was not specified properly or only one range when calling multipleRange search")
    
    s = Search()       
    query_list = [] 
    path_to_search = None #this will be set if it is a nested search
    #take each of the range conditions
    for single_range_condition in range_conditions_list:
        #seperate at the # to get the location and the range condition parts
        parts = single_range_condition.split("#")
        #fill the range conditions into range_param_dict             
        range_info_string = parts[1]
        range_info_string = range_info_string.replace("[","")        
        constraints_parts = range_info_string.split(",")
        range_param_dict = {} 
        for i in range(0,len(constraints_parts)):
            constraints_parts[i] = constraints_parts[i].replace(" " , "")                
            rangeParts = constraints_parts[i].split(":")
            range_param_dict[rangeParts[0]] = rangeParts[1]    
                    
        path_parts = parts[0].split("/")
        area_to_search = ".".join(path_parts) #+ ["_all"])
        q = None
        #check if this is a nested search, i.e. the path has "/"
        if len(path_parts) > 1:
            path_to_search = ".".join(path_parts[:-1])                        
        range_search_dict = {area_to_search:range_param_dict}                                    
        q =Q('range',**range_search_dict)
    
        query_list.append(q)
    #---END FOR LOOP
    nested_query = Q('bool',should = query_list)
    main_query = None
    if path_to_search != None:
        path_to_search = path_to_search.replace(" ","")
        main_query = Q("nested", path = path_to_search, query = nested_query )
    else:
        main_query = nested_query 
    s = s.query(main_query)
    print("running multiple range query on many fields \n", s.to_dict())    
    response = s.execute()
    return response

#===========================================================================
# 
#===========================================================================

def execute_pylastic_mixed_search(input_string):
    '''
    
    @param inputString: expect a combination of range and boolean searches
    @summary: Does the following type of search which has many ranged fields. 
    can be nested too, but then all must be of the same nesting.
        "query": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                "created_at": {
                                    "gte": "2013-12-09T00:00:00.000Z"
                                }
                            }
                        },
                        {
                            "match": {
                                "city": "new york"                                                                
                            }
                        }
                    ]
                }
            }
    '''
    
    conditions_list = input_string.split("]")
    #next remove the last one as it will be '' empty string
    conditions_list = conditions_list[:-1]
    if "[" not in input_string and "]" not in input_string :
        raise(Exception,\
            "Range was not specified properly or only one range when calling multipleRange search")
    
    s = Search()       
    query_list = [] 
    path_to_search = None #this will be set if it is a nested search
    #take each of the range conditions
    for single_condition in conditions_list:
        #seperate at the # to get the location and the range condition parts
        parts = single_condition.split("#")
        #fill the range conditions into range_param_dict             
        value_string = parts[1]
        if ":" in value_string:
            range_info_string = value_string
            range_info_string = range_info_string.replace("[","")        
            constraints_parts = range_info_string.split(",")
            range_param_dict = {} 
            for i in range(0,len(constraints_parts)):
                constraints_parts[i] = constraints_parts[i].replace(" " , "")                
                rangeParts = constraints_parts[i].split(":")
                range_param_dict[rangeParts[0]] = rangeParts[1]                        
            path_parts = parts[0].split("/")
            area_to_search = ".".join(path_parts) #+ ["_all"])
            q = None
            #check if this is a nested search, i.e. the path has "/"
            if len(path_parts) > 1:
                path_to_search = ".".join(path_parts[:-1])                        
            range_search_dict = {area_to_search:range_param_dict}                                    
            q =Q('range',**range_search_dict)    
            query_list.append(q)
        else: #it is a boolean query
            #similar process except no range dict. If there is a comma, 
            # create multiple boolean queries searches on that field.
            term_info_string = value_string
            term_info_string = term_info_string.replace("[","")        
            term_list = term_info_string.split(",")            
            for single_term in term_list:
                #do NOT replace spaces as they maybe part of the phrase to search for                                                                                                    
                path_parts = parts[0].split("/")
                area_to_search = ".".join(path_parts) #+ ["_all"])
                q = None
                #check if this is a nested search, i.e. the path has "/"
                if len(path_parts) > 1:
                    path_to_search = ".".join(path_parts[:-1])                                                                            
                q =Q('match', **{area_to_search : single_term})    
                query_list.append(q)            
    #---END FOR LOOP
    nested_query = Q('bool',should = query_list)
    main_query = None
    if path_to_search != None:
        path_to_search = path_to_search.replace(" ","")
        main_query = Q("nested", path = path_to_search, query = nested_query )
    else:
        main_query = nested_query 
    s = s.query(main_query)
    print("running multiple range query on many fields \n", s.to_dict())    
    response = s.execute()
    return response

    
#===============================================================================
# 
#===============================================================================
def add_additional_UI_info(list_dicts):
    '''
    @summary: This is for helping the UI. For now it just adds a unique id for each entry
    '''
    id_num = 0
    for each_dict in list_dicts:
        id_num += 1
        each_dict['id'] = id_num        
#===============================================================================
# 
#===============================================================================


#===============================================================================
# 
#===============================================================================
print("END of Pylastic Interface initialization, can now use functions")
