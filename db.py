from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200") #this is the port where elasticserach runs
print(es.info().body)