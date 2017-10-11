#   Copyright 2017 Joe Talerico
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


import elasticsearch
import datetime

class Elastic(object):
    def __init__(self,elastichost, port=9200):
        self.es = elasticsearch.Elasticsearch([{'host': elastichost,
             'port': port}],send_get_body_as='POST')

    def search(self, index, query):
        data = self.es.search(index=index,
                body=query)
        return data

    def index(self,payload,index,_type='doc') :
        if payload is None :
            return False
        now = datetime.datetime.utcnow()
        payload['insert_timestamp'] = now
        return self.es.index(index,_type,payload)
