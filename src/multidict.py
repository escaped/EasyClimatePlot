class MultiDict(dict):
    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except:
            return self.setdefault(key, MultiDict()) 
