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

from Clouds import Clouds
from Hosts import Hosts
from History import History
from CloudHistory import CloudHistory

class QuadsData(object):
    def __init__(self, data):
        """
        Initialize the QuadsData object.
        """
        self.hosts = Hosts(data)
        self.clouds = Clouds(data)
        self.history = History(data)
        self.cloud_history = CloudHistory(data)
