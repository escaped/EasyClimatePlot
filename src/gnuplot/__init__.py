import os
import tempfile
import random
import subprocess


class Tempfile(object):  
  def getFilename(self):
    fd, self.path = tempfile.mkstemp(prefix=self.__class__.__name__+"_")
    os.write(fd, self.content)
    os.close(fd)
    return self.path

  def deleteFile(self):
    if self.path != None:
      os.remove(self.path)
      self.path = None



class GnuplotData(Tempfile):
  def __init__(self, data, type):
    self.content = ''
    if type == "m":
      for month in range(0,12):
        self.content += str(month+1)+"\t"
        for d in data:
          if d == None:
            self.content += "\t"
          else:
            self.content += str('%.2f' %d[month])+"\t"
        self.content += "\n"



class GnuplotTemplate(Tempfile): 
  def __init__(self, file):
    print file
    if not os.path.isfile(file):
      raise ValueError
    fd = open(file, 'r')    
    self.content = fd.read()
    fd.close() 

  def replace(self, pattern, value):
    self.content = self.content.replace(pattern, value)
  
  def setOutput(self, file):
    self.replace('{{OUTPUT}}', file) 
    
  def setTitle(self, title):
    self.replace('{{TITLE}}', title) 


class Gnuplot(object):
  def plot(self, template, data):
    i = 0
    for d in data:
      if i == 0:
        template.replace('{{DATA}}', d.getFilename().replace('\','/')) 
      else:
        template.replace('{{DATA'+i+'}}', d.getFilename().'\','/')) 
      i = i+1
      
    gpfile = template.getFilename()
    print template.content

    subprocess.call(['gnuplot', gpfile])
    
    #template.deleteFile()
    #for d in data:
    #  d.deleteFile()
