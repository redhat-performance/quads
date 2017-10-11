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

import Elastic
import KerberosTicket
import requests
from dateutil.parser import parse


class RTQuery(object):

    def __init__(self, config):
        self.CONFIG = config
        self.es = Elastic.Elastic(
            self.CONFIG['elastichost'], self.CONFIG['elasticport'])

    def _query(self, url, querystring=None):
        krb = KerberosTicket.KerberosTicket(self.CONFIG['domain'])
        headers = {"Authorization": krb.auth_header}
        if querystring is None:
            req = requests.get(url, headers=headers, verify=False)
        else:
            req = requests.get(url, headers=headers,
                               params=querystring, verify=False)
        return req

    def _push(self, url, payload):
        krb = KerberosTicket.KerberosTicket(self.CONFIG['domain'])
        headers = {"Authorization": krb.auth_header}
        req = requests.get(url, headers=headers,
                           params=payload, data=payload, verify=False)
        return req

    def rt_search(self, querystring):
        url = "{}".format(self.CONFIG['urls']['search'])
        r = self._query(url, querystring)
        lab_requests = {}
        for line in r.text.split('\n'):
            if ':' in line:
                values = line.split(":")
                lab_requests[str(values[0].strip())] = str(values[1].strip())
        return lab_requests

    def rt_history_comment(self, ticket, message):
        url = "{}/{}/comment".format(self.CONFIG['urls']['ticket'], ticket)
        payload = {'content': {"Action: comment\nText: {}".format(message)}}
        return self._push(url, payload).text

    def es_insert_rt(self, rt_id, request):
        if len(self.es_search_rt(rt_id)) is 0:
            return self.es.index(request, self.CONFIG['index'])

    def es_search_rt(self, rt_id):
        query = {"query": {"match": {"ticket": rt_id}}}
        req = self.es.search(self.CONFIG['index'], query)
        return req['hits']['hits']

    def rt_history(self, rt_id):
        history = []
        url = "{}/{}/history".format(self.CONFIG['urls']['ticket'], rt_id)
        r = self._query(url)
        for line in r.text.split('\n'):
            if ':' in line:
                hist = {}
                values = line.split(":")
                if len(values) > 2:
                    hist['id'] = str(values[1].strip())
                    hist['desc'] = str(values[2].strip())
                else:
                    hist['id'] = str(values[0].strip())
                    hist['desc'] = str(values[1].strip())
                history.append(hist)
        return history

    def rt_history_query(self, rt_id, hist_id):
        url = "{}/{}/history/id/{}".format(
            self.CONFIG['urls']['ticket'], rt_id, hist_id)
        r = self._query(url)
        request = {}
        for line in r.text.split('\n'):
            if ':' in line:
                values = line.split(":", 1)
                if values[1].count(':') is 1:
                    values = values[1].split(":", 1)
                    request[str(values[0].encode('utf-8').strip())
                            ] = str(values[1].encode('utf-8').strip())
                else:
                    request[str(values[0].encode('utf-8').strip())
                            ] = str(values[1].encode('utf-8').strip())
        return request

    def rt_es_mapper(self, request):
        products = {'Openstack': 'OpenStack',
                    'RHOP': 'OpenStack',
                    'OpenStack RHOSP-11': 'OpenStack',
                    'Red Hat OpenStack Newton (10)': 'OpenStack',
                    'openstack': 'OpenStack',
                    'OSP 11': 'OpenStack',
                    'Openstack, TripleO': 'OpenStack',
                    'Red Hat OpenStack Platform': 'Openstack',
                    'RedHat Openstack': 'OpenStack',
                    'rhel osp': 'OpenStack',
                    'Red Hat OpenStack Ocata (11)': 'OpenStack'}
        mapper = {'timestamp': request['Created'],
                  'author': request['Creator'],
                  'description': request['Description'],
                  'ticket': request['Ticket'],
                  'id': request['id']}
        if 'Use Case' in request:
            mapper['use'] = request['Use Case'],
        if 'are you targeting to improve?' in request:
            mapper['use'] = request['are you targeting to improve?']
        else:
            mapper['use'] = 'unknown'
        if 'Red Hat product(s) being tested' in request:
            mapper['product'] = request['Red Hat product(s) being tested']
        elif 'Performance Red Hat product(s) being tested' in request:
            mapper['product'] = request[
                'Performance Red Hat product(s) being tested']
        else:
            mapper['product'] = 'unknown'
        if 'Number of nodes being requested' in request:
            mapper['node_count'] = request['Number of nodes being requested'].split(" ")[
                0]
        elif 'being requested' in request:
            mapper['node_count'] = request['being requested'].split(" ")[0]
        elif 'Platform Number of nodes being requested' in request:
            mapper['node_count'] = request[
                'Platform Number of nodes being requested'].split(" ")[0]
        else:
            mapper['node_count'] = 0,
        if mapper['product'] in products:
            mapper['product'] = products[mapper['product']]
        return mapper
