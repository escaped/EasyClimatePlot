class MultiDict(dict):
    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except:
            return self.setdefault(key, MultiDict()) 


from collections import defaultdict

class Dict(defaultdict):
    def __init__(self, args = None):
        defaultdict.__init__(self, Dict)

    def __repr__(self):
        return dict.__repr__(self)