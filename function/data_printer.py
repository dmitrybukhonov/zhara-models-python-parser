import sys
import pprint

class dd:
    def __init__(self, data):
        self.data = data
        self.pp = pprint.PrettyPrinter(indent=4)
        self.pp.pprint(self.data)
        sys.exit(1)
        
