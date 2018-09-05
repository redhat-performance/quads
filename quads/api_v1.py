# This file is part of QUADs.
#
# QUADs is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# QUADs is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with QUADs.  If not, see <http://www.gnu.org/licenses/>.


import json
import cherrypy
import time
import urllib

from quads.quads import Quads
from quads.helpers import param_check

# Setup Jinja Templates
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('templates'))

LSACTIONS = ['lshosts', 'lsclouds', 'lsowner', 'lsowners', 'lsccusers',
             'lstickets', 'lsqinq', 'lswipe']
OTHERS = ['host', 'rmhost', 'cloud', 'rmcloud', 'ahs',
          'rhs', 'mhs', 'moves', 'query']


class QuadsServer(object):
    def __init__(self, config, statedir, initialize, force, write_lock):
        self.quads = Quads(config, statedir, None, None,
                           None, initialize, force, write_lock)
        self.write_lock = write_lock

    @cherrypy.expose
    def index(self):
        tmpl = env.get_template('index.html')
        return tmpl.render(session=cherrypy.session)

    @cherrypy.expose
    def v1(self, action, **data):
        # api consistency fix:
        if action == 'lsowner':
            action = 'lsowners'
        if action == 'lsccusers':
            action = 'cc'

        # set response type to json
        cherrypy.response.headers['Content-Type'] = 'application/json'

        # TODO: figure out why this isn't coming in **data
        # POST data not being processed properly.
        #      doing it manually
        raw = cherrypy.request.body.readlines()
        if raw:
            decoded = urllib.unquote_plus(raw[0])
            data = dict(map(lambda z: z.split('='), decoded.split('&')))
        else:
            data = {}

        # handle requests
        print(action)

        if action in LSACTIONS:
            if action[:2] == 'ls':
                action = action[2:]

            if 'cloudonly' in data:
                if action[-1] == 's':
                    action = action[:-1]
                data = data['cloudonly']

            func = getattr(self.quads, 'get_%s' % action)
            # api consitency fix
            key = 'qinqs' if action == 'qinq' else action
            ret_data = {key: func(data)} if data else {key: func()}
            return json.dumps(ret_data)

        elif action in OTHERS:
            func = getattr(self, action)
            return func(data)
        else:
            raise cherrypy.NotFound()

    def host(self, data):
        result, data = param_check(data, ['host', 'cloud', 'force', 'type'])
        if len(result) > 0:
            return json.dumps({'result': result})
        self.write_lock.acquire()
        result = self.quads.update_host(data['host'],
                                        data['cloud'],
                                        data['type'],
                                        data['force'] == 'True')
        self.write_lock.release()
        return json.dumps({'result': result})

    def rmhost(self, data):
        result, data = param_check(data, ['host'])
        if len(result) > 0:
            return json.dumps({'result': result})
        self.write_lock.acquire()
        print(data['host'])
        result = self.quads.remove_host(data['host'])
        self.write_lock.release()
        return json.dumps({'result': result})

    def cloud(self, data):
        defaults = {'owner': 'nobody',
                    'cc': [[]],
                    'ticket': ['000000'],
                    'qinq': ['0'],
                    'wipe': ['1']}

        result, data = param_check(data,
                                   ['cloud', 'description', 'force',
                                    'owner', 'cc', 'ticket', 'qinq',
                                    'wipe'],
                                   defaults)
        if len(result) > 0:
            return json.dumps({'result': result})
        self.write_lock.acquire()
        result = self.quads.update_cloud(data['cloud'],
                                         data['description'],
                                         data['force'] == 'True',
                                         data['owner'],
                                         data['cc'][0],
                                         data['ticket'],
                                         data['qinq'],
                                         data['wipe'])
        self.write_lock.release()
        return json.dumps({'result': result})

    def rmcloud(self, data):
        result, data = param_check(data, ['cloud'])
        if len(result) > 0:
            return json.dumps({'result': result})
        self.write_lock.acquire()
        result = self.quads.remove_cloud(data['cloud'][0])
        self.write_lock.release()
        return json.dumps({'result': result})

    def ahs(self, data):
        result, data = param_check(data, ['start', 'end', 'cloud', 'host'])
        if len(result) > 0:
            return json.dumps({'result': result})
        self.write_lock.acquire()
        result = self.quads.add_host_schedule(data['start'],
                                              data['end'],
                                              data['cloud'],
                                              data['host'])
        self.write_lock.release()
        return json.dumps({'result': result})

    def rhs(self, data):
        result, data = param_check(data, ['schedule', 'host'])
        if len(result) > 0:
            return json.dumps({'result': result})
        self.write_lock.acquire()
        result = self.quads.rm_host_schedule(int(data['schedule']),
                                             data['host'])
        self.write_lock.release()
        return json.dumps({'result': result})

    def mhs(self, data):
        defaults = {'start': None,
                    'end': None,
                    'cloud': None}

        # TODO: does passing None defaults work ok here? I think so....
        result, data = param_check(data,
                                   ['schedule', 'host',
                                    'start', 'end', 'cloud'],
                                   defaults)
        if 'start' not in data and 'end' not in data and 'cloud' not in data:
            result.append("Must have at least one of: start, end, cloud")
        if len(result) > 0:
            return json.dumps({'result': result})
        self.write_lock.acquire()
        result = self.quads.mod_host_schedule(int(data['schedule']),
                                              data['start'],
                                              data['end'],
                                              data['cloud'],
                                              data['host'])
        self.write_lock.release()
        return json.dumps({'result': result})

    def moves(self, data):
        defaults = {'date': time.strftime("%Y-%m-%d %H:%M"),
                    'wipe': ['1']}

        result, data = param_check(data, ['date', 'statedir'], defaults)
        if len(result) > 0:
            return json.dumps({'result': result})
        result = self.quads.pending_moves(data['statedir'],
                                          data['date'])
        return json.dumps({'result': result})

    def query(self, data):
        defaults = {'date': None,
                    'host': None,
                    'cloud': None,
                    'summary': None,
                    'fullsummary': None,
                    'lsschedule': None}
        result, data = param_check(data,
                                   defaults.keys(),
                                   defaults)
        if len(result) > 0:
            return json.dumps({'result': result})
        if data['host'] is not None:
            if data['lsschedule'] == 'True':
                default_cloud, current_cloud, current_schedule, full_schedule =\
                        self.quads.query_host_schedule(data['host'],
                                                       data['date'])
                result.append("Default cloud: {}".format(default_cloud))
                result.append("Current cloud: {}".format(current_cloud))
                if current_schedule is not None:
                    result.append("Current schedule: {}".format(current_schedule))
                if len(full_schedule) > 0:
                    for item in full_schedule:
                        for override, schedule in item.items():
                            output = " {}| ".format(override)
                            for t, date in schedule.items():
                                if t == 'start' or t == 'end':
                                    output += "{}={},".format(t, date)
                                else:
                                    output += "{}={}".format(t, date)
                            result.append(output)
            else:
                result.append(self.quads.query_host_cloud(data['host'],
                                                          data['date']))
            return json.dumps({'result': result})

        if data['summary'] == 'True' and data['fullsummary'] == 'True':
            result.append("--summary and --full-summary"
                          "are mutually exclusive.")
            return json.dumps({'result': result})

        if data['summary'] == 'True' or data['fullsummary'] == 'True':
            if data['fullsummary'] == 'True':
                cloud_summary = self.quads.query_cloud_summary(data['date'],
                                                               False)
            else:
                cloud_summary = self.quads.query_cloud_summary(data['date'],
                                                               True)
            if len(cloud_summary) > 0:
                for item in cloud_summary:
                    for cloudname, details in item.items():
                        r = cloudname + " : "
                        for param, description in details.items():
                            if param == 'hosts':
                                r += str(description) + " "
                            else:
                                if param == 'description':
                                    r += "({})".format(description)
                        result.append(r)
        else:
            cloud_hosts = self.quads.query_cloud_hosts(data['date'])
            if data['cloud'] is not None:
                if data['cloud'] in cloud_hosts:
                    for host in cloud_hosts[data['cloud']]:
                        result.append(host)
                else:
                    result.append("Requested cloud does not exist")
            else:
                for cloud, hostlist in sorted(cloud_hosts.items()):
                    result.append("{}:".format(cloud))
                    for host in hostlist:
                        result.append(" - {}".format(host))

        return json.dumps({'result': result})
