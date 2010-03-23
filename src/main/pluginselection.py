'''
Created on Mar 23, 2010

@author: alex
'''
import wx
from wxcustom.panel import Panel

from pluginmanager import PluginManager


class PluginSelection(Panel):
  def __init__(self, *args, **kwargs):
    Panel.__init__ (self, *args, **kwargs)

    self.pm = PluginManager.getInstance()
    
    # List
    self.list = wx.ListBox(choices=self.pm.getInputPlugins().keys(), parent=self, size=wx.Size(150, 200), style=0)
    self.list.Bind(wx.EVT_LISTBOX, self.OnListBox1Listbox)
    
    # Infobox
    info = wx.StaticBox(self, -1, "Plugin Info", size=wx.Size(400,100))
    labelSizer = wx.GridSizer(4, 2, 2, 1)
    
    labelSizer.Add(wx.StaticText(self, -1, "Name: "))
    self.lblName = wx.StaticText(self, -1, "")
    labelSizer.Add(self.lblName)
    
    labelSizer.Add(wx.StaticText(self, -1, "Version: "))
    self.lblVersion = wx.StaticText(self, -1, "")
    labelSizer.Add(self.lblVersion)
    
    labelSizer.Add(wx.StaticText(self, -1, "Author: "))
    self.lblAuthor = wx.StaticText(self, -1, "")
    labelSizer.Add(self.lblAuthor)
    
    labelSizer.Add(wx.StaticText(self, -1, "Description: "))
    self.lblDescription = wx.StaticText(self, -1, "")
    labelSizer.Add(self.lblDescription)
    
    infoSizer = wx.StaticBoxSizer(info, wx.VERTICAL)
    infoSizer.Add(labelSizer)
    
    # put all together
    mainSizer = wx.BoxSizer(wx.HORIZONTAL)
    mainSizer.Add(self.list, 0, wx.EXPAND, 0)
    mainSizer.Add(infoSizer, 0, wx.EXPAND, 0)
    
    self.SetSizer (mainSizer)
    self.Layout()
  
  def OnListBox1Listbox(self, event):
    pluginName = self.list.GetStringSelection()
    print "Selected: %s" %(pluginName)
    if pluginName != None:
      try: 
        plugin = self.pm.getInputPlugins()[pluginName]
      except KeyError:
        self.clearInfo()
        return
      
      self.lblName.SetLabel(plugin.getName())
      self.lblVersion.SetLabel(plugin.getVersion())
      self.lblAuthor.SetLabel(plugin.getAuthor())
      self.lblDescription.SetLabel(plugin.getDescription())   
    else:
      self.clearInfo()
      
  def clearInfo(self):
      self.lblName.SetLabel("")
      self.lblVersion.SetLabel("")
      self.lblDescription.SetLabel("")   
      self.lblAuthor.SetLabel("")