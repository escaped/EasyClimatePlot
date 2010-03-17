import config
import os
import cPickle
import hashlib
import utils


            
def test():
    cache = CacheManager()
    import data
    d1 = data.Data('33','coord')
    d2 = data.Data('34','coord')

    dd = utils.Dict()
    for i in range(1966,2010):
        dd['temp'][str(i)+'1033'] = 10
        dd['precipitation'][str(i)+'1033'] = 20
        if 1985 <= i and i <= 1990:
            dd['wind'][str(i)+'1033'] = 33  
    
    d1.addCategory('temp', dd['temp'])    
    d1.addCategory('precipitation', dd['precipitation'])
    
    cache.save(d1, "noaa", 33, '19661033', '20101033')
    cache.loadIndex()
    d1_1 = cache.load('noaa', 33, '19661033', '20101033')
    d1_2 = cache.load('noaa', 33, '19701033', '20001033')
    d1_3 = cache.load('noaa', 33, '19701033', '20121033')
    
    print "d1 ist:"
    print d1._getData()
    print "dumps;"
    print d1_1
    print d1_1._getData()
    print
    print d1_2._getData()
    print
    print d1_3
    
    d2.addCategory('wind', dd['wind'])
    
    cache.save(d2, "noaa", 34, '19851033', '19901033')
    cache.loadIndex()
    d2_1 = cache.load('noaa', 34, '19851033', '19901033')
    d2_2 = cache.load('noaa', 34, '19851033', '19901033')
    d2_3 = cache.load('noaa', 34, '19701033', '19901033')
    
    print "d2 ist:"
    print d2.data
    print "dumps;"
    print d2_1._getData()
    print
    print d2_2._getData()
    print
    print d2_3

class CacheManager(object):
    
    index = utils.Dict()
    indexFilename= os.path.join (config.CACHEDIR, config.CACHE_INDEX_FILENAME)
    
    def __init__(self):
        # checkPathes
        utils._mkdir(config.CACHEDIR)
        
        # load index-Hashtable
        if os.path.isfile(self.indexFilename):
            self.loadIndex()
    
    def loadIndex(self):
        try:
            f = open(self.indexFilename, "r")
            self.index = cPickle.load(f)
            f.close()
        except:
            pass
    
    def saveIndex(self):
        try:
            f = open(self.indexFilename, "w")
            cPickle.dump(self.index,f)
            f.close()
        except:
            pass    
    
    def hash(self, str):
        return hashlib.md5(str).hexdigest()
    
    def load(self, module, id, starttime, endtime):
        obj = None
        for key in self.index[module][id]:
            if key[0] <= starttime and endtime <= key[1]:
                f = open(os.path.join(config.CACHEDIR, module, self.index[module][id][key]), "r")
                obj = cPickle.load(f)
                f.close()
                break
        return obj
                
    
    def save(self, obj, module, id, starttime, endtime):
        filename = self.hash(str(id)+starttime+endtime)
        
        #create dirs if not exist
        dir = os.path.join(config.CACHEDIR, module)
        utils._mkdir(dir)
        
        # store data
        f = open(os.path.join(dir, filename), "w")
        cPickle.dump(obj,f)
        f.close()
        
        # add to index
        self.index[module][id][(starttime,endtime)] = filename
        self.saveIndex()
    
    
        