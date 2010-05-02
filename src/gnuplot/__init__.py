import os
import tempfile
import random
import subprocess


class Tempfile(object):
  
  def getFile(self):
    fd, self.path = tempfile.mkstemp(prefix=self.__class__.__name__+"_")
    os.write(fd, self.content)
    os.close(fd)
    return self.path

  def deleteFile(self):
    if self.path != None:
      os.remove(self.path)
      self.path = None



class GnuplotData(object):
  pass



class GnuplotTemplate(Tempfile): 
  def init(self, file, data):
    if not os.path.isfile(file):
      raise ValueError
    
    self.content = open(file, 'r').read() 
    self.data = data
  
  def setOutputfile(self, file):
    self.content.replace('{{OUTPUT}}', file)
    
  def replace(self, pattern, value):
    self.content.replace(pattern, value)


class Gnuplot(object):
  def init(self, template):
    self.template = template
    
  def plot(self, filename):
    self.template.setTerminal('png')
    self.template.setOutputfile(filename+'png')
    
    gpfile = self.template.getFile()

    subprocess.call(['gnuplot', gpfile])
    self.template.deleteFile()