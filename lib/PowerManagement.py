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

import abc

class PowerManagement(object):

    __metaclass__ = abc.ABCMeta

    brands = ['ServerTech','Apc']

    @abc.abstractmethod
    def on(self):
        pass

    @abc.abstractmethod
    def off(self):
        pass

    @abc.abstractmethod
    def drain(self):
        pass

    @classmethod
    @abc.abstractmethod
    def get_brands(cls):
        return cls.brands
