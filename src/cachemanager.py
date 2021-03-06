import config
import os
import cPickle
import hashlib
import utils
from singletonmixin import Singleton

class CacheManager(Singleton):
    
    index=utils.Dict()
    indexFilename=os.path.join (config.CACHEDIR, config.CACHE_INDEX_FILENAME)
    
    def __init__(self):
        # checkPathes
        utils._mkdir(config.CACHEDIR)
        
        # load index-Hashtable
        if os.path.isfile(self.indexFilename):
            self.loadIndex()
    
    # TODO enhance exception handling - don't catch _everything_
    def loadIndex(self):
        try:
            f=open(self.indexFilename, "r")
            self.index=cPickle.load(f)
            f.close()
        except:
            pass
    
    def saveIndex(self):
        try:
            f=open(self.indexFilename, "w")
            cPickle.dump(self.index, f)
            f.close()
        except:
            pass    
    
    def hash(self, str):
        return hashlib.md5(str).hexdigest()
      
    # TODO module should be the PluginName!
    def load(self, module, id, starttime = None, endtime = None):
        print "load obj for (%s, %s)" %(module, id)
        obj=None
        
        for key in self.index[module][str(id)]:
            if key[0]<=starttime and endtime<=key[1]:
                f=open(os.path.join(config.CACHEDIR, module, self.index[module][str(id)][key]), "r")
                obj=cPickle.load(f)
                f.close()
                break

        return obj
    
    def save(self, obj, module, id, starttime = None, endtime = None):
        print "save obj for (%s, %s)" %(module, id)
        if starttime==None or endtime==None:
            filename=self.hash(str(id))
        else:
            filename=self.hash(str(id)+str(starttime)+str(endtime))
        
        #create dirs if not exist
        dir=os.path.join(config.CACHEDIR, module)
        utils._mkdir(dir)
        
        # store data
        f=open(os.path.join(dir, filename), "w")
        cPickle.dump(obj, f)
        f.close()
        
        # add to index
        if starttime==None or endtime==None:
            self.index[module][str(id)]=filename
        else:
            self.index[module][str(id)][(starttime, endtime)]=filename
        self.saveIndex()
    
    def hashExists(self, module, id, starttime = None, endtime = None):
        print "checking for (%s, %s)" %(module, id)
        if starttime==None or endtime==None:
            if isinstance(self.index[module][str(id)], str):
                return 1
        else:
            if isinstance(self.index[module][str(id)][(starttime, endtime)], str):
                return 1
        return 0

    def delete (self, module, id, starttime = None, endtime = None):
      print "deleteing %s" %id
      index = self.index[module]
      if starttime==None or endtime==None:
          filename = index[str(id)]
          del index[str(id)]
      else:
          filename = index[str(id)][(starttime, endtime)]
          del index[str(id)][(starttime, endtime)]

      # try to delete the file
      dir=os.path.join(config.CACHEDIR, module)
      try:
        os.remove (os.path.join (dir,filename))
      except AttributeError:
        # we maybe received a dict? if not, nvm
        for item in filename.values ():
          os.remove (os.path.join (dir, item))

      self.saveIndex ()
    
def test():
    cache=CacheManager.getInstance()
    import data
    d1=data.Data('31', 'coord')
    d2=data.Data('34', 'coord')

    dd=utils.Dict()
    for i in xrange(1966, 2010):
        dd['temp'][str(i)+'1031']=10
        dd['precipitation'][str(i)+'1031']=20
        if 1985<=i and i<=1990:
            dd['wind'][str(i)+'1031']=31  
    
    d1.addCategory('temp', dd['temp'])    
    d1.addCategory('precipitation', dd['precipitation'])
    
    cache.save(d1, "noaa", 31, '19661031', '20101031')
    cache.loadIndex()
    d1_1=cache.load('noaa', 31, '19661031', '20101031')
    d1_2=cache.load('noaa', 31, '19701031', '20001031')
    d1_3=cache.load('noaa', 31, '19701031', '20121031')
    
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
    
    cache.save(d2, "noaa", 34, '19851031', '19901031')
    cache.loadIndex()
    d2_1=cache.load('noaa', 34, '19851031', '19901031')
    d2_2=cache.load('noaa', 34, '19851031', '19901031')
    d2_3=cache.load('noaa', 34, '19701031', '19901031')
    
    print "d2 ist:"
    print d2.data
    print "dumps;"
    print d2_1._getData()
    print
    print d2_2._getData()
    print
    print d2_3

def delete ():
  # delete the first cached item
  cache = CacheManager.getInstance ()
  print cache.index
  cache.delete ('noaa', cache.index['noaa'].keys ()[0]) 

# call test function
if __name__=="__main__":
  test ()
  delete ()
