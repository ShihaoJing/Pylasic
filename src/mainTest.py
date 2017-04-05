
import elasticsearch

from elasticsearch_dsl.connections import connections
import httplib

connections.create_connection(hosts=['localhost:9200'], timeout=20)



conn = httplib.HTTPConnection("localhost:9200")
conn.request("GET","/")
res = conn.getresponse()
print res.status, res.reason
print res.read()

'''
NEXT:
Create some dummy documents in JSON (py dict) format), and execute a filter query.
use the dsl library
'''


print("END of elastic search test script")