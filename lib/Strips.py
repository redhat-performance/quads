#   Copyright 2017 Joe Talerico
#

import logging

class Strips(object):
    def __init__(self, data):
        """
        Initialize a Hosts object. This is a subset of
        data required by the Quads object.
        """
        self.logger = logging.getLogger("Quads.Strips")
        self.logger.setLevel(logging.DEBUG)
        if 'strips' not in data:
            self.logger.error("data missing required \"Strips\" section.")
            exit(1)

        self.data = data["strips"]

    # return list of strips
    def get(self):
        return sorted(self.data.iterkeys())
