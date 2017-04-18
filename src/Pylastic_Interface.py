
'''
@summary: This script contains the functions that allow the Pylastic flask web server
to search and get results from the Elastic Search instance/node that is running
'''


import httplib
import csv2es
import pyelasticsearch
import elasticsearch
from elasticsearch import Elasticsearch
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Search, Q


connections.create_connection(hosts=['localhost:9200'], timeout=20)


def execute_pylastic_search(input_string, **kwargs):
    '''
    @param input_string: the user's query string
    @param **kwargs: Key word arguments that define the query. eg: type = 'bool' will run a boolean query
    @return: an ordered list of results. [{doc1 info}, {doc2 info},....]
            each doc info contains the "name", "URL", "snippet". snippet contains the matching parts of the doc.
    '''
    if 'type' in kwargs:
        if kwargs['type'] == 'bool':
            return execute_pylastic_boolean_search(input_string)
#END FUNCTION

def execute_pylastic_boolean_search(input_string):
    '''
    '''
    s = Search()
    q = Q('bool',must=[Q('match', CITY='San Francisco')])    
    s = s.query(q)
    print("running boolean query \n", s.to_dict())    
    response = s.execute()
    return response






print("END of Pylastic Interface initialization, can now use functions")
