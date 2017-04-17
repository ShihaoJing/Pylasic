
'''
@summary: This script contains the functions that allow the Pylastic flask web server
to search and get results from the Elastic Search instance/node that is running
'''


def execute_pylastic_search(input_string, **kwargs):
    '''
    @param input_string: the user's query string
    @param **kwargs: Key word arguments that define the query. eg: type = 'bool' will run a boolean query
    @return: an ordered list of results. [{doc1 info}, {doc2 info},....]
            each doc info contains the "name", "URL", "snippet". snippet contains the matching parts of the doc.
    '''
    pass