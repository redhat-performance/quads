import elasticsearch
import datetime

class Elastic(object):
    def __init__(self,elastichost, port=9200):
        self.es = elasticsearch.Elasticsearch([{'host': elastichost,
             'port': port}],send_get_body_as='POST')

    def index(self,payload,index,_type='log') :
        now = datetime.datetime.utcnow()
        payload['timestamp'] = now
        return self.es.index(index,_type,payload)
