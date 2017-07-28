#   Copyright 2017 Joe Talerico
#

import logging
import copy

class Strips(object):
    def __init__(self, data=None):
        """
        Initialize a Strips object. This is a subset of
        data required by the Quads object. (used for PDU
        tracking)
        """
        self.logger = logging.getLogger("quads.Strips")
        self.logger.setLevel(logging.DEBUG)
        if data is None:
            self.data = {}
            return

        if 'strips' not in data:
            self.logger.error("data missing required \"strips\" section.")
            self.data = {}
            return

        self.data = copy.deepcopy(data["strips"])

    def put(self, data):
        if 'strips' not in data:
            self.logger.error("data missing required \"strips\" section.")
            self.data = {}
            return

        self.data = copy.deepcopy(data["strips"])

    # return list of strips
    def get(self):
        return sorted(self.data.iterkeys())

