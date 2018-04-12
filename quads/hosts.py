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

import logging
import copy


class Hosts(object):
    def __init__(self, data=None):
        """
        Initialize a Hosts object. This is a subset of
        data required by the Quads object.
        """
        self.logger = logging.getLogger("quads.Hosts")
        self.logger.setLevel(logging.DEBUG)
        if data is None:
            self.data = {}
            return

        if 'hosts' not in data:
            self.logger.error("data missing required \"hosts\" section.")
            self.data = {}
            return

        self.data = copy.deepcopy(data["hosts"])

    def put(self, data):
        if 'hosts' not in data:
            self.logger.error("data missing required \"hosts\" section.")
            self.data = {}
            return

        self.data = copy.deepcopy(data["hosts"])

    # return list of hosts
    def get(self):
        return sorted(self.data.iterkeys())
