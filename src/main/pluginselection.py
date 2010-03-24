'''
Created on Mar 23, 2010

@author: alex
'''
from mvc.control import Control
from mvc.workflow.hook import Hook
from mvc.workflow.wizard import Wizard

import wx
from wxcustom.panel import Panel
from wxcustom.error import ErrorMessage

from pluginmanager import PluginManager

class NotEmptyValidator (wx.PyValidator):
  def __init__(self, msg = "Field cannot be empty."):
    wx.PyValidator.__init__(self)    
    self.errorMsg = msg
  
  def TransferToWindow(self):
    return True # Prevent wxDialog from complaining.

  def TransferFromWindow(self):
    return True # Prevent wxDialog from complaining.
    
  def Clone(self):
    return NotEmptyValidator()
  
  def Validate(self, win):
    item = self.GetWindow()
    value = item.GetValue()
    
    if len(value) == 0:
      ErrorMessage (self.errorMsg)
      item.SetFocus()
      return False
    
    return True

class PluginSelectionControl (Control):
  def __init__ (self, view):
    Control.__init__ (self, view)
    
  def onDeactivate(self):
    ''' Check Input '''
    if self.view.Validate():
      # TODO add views from Plugin
      return True
    return False
  
class PluginSelectionPanel(Panel):
  def __init__(self, *args, **kwargs):
    Panel.__init__ (self, *args, **kwargs)

    self.pm = PluginManager.getInstance()
    
    # List
    listSizer = wx.BoxSizer(wx.VERTICAL)
    self.list = wx.ListBox(choices=self.pm.getInputPlugins().keys(), parent=self, size=wx.Size(150, 200), validator=NotEmptyValidator("Please select a plugin."))
    self.list.Bind(wx.EVT_LISTBOX, self.OnListBox1Listbox)
    
    listSizer.Add(wx.StaticText(self, -1, "Select Plugin:"), 0, wx.EXPAND, 0)
    listSizer.Add(self.list, 0, wx.EXPAND, 0)
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
    infoSizer.Add(labelSizer, 0, wx.EXPAND, 0)
    
    # put all together
    mainSizer = wx.BoxSizer(wx.HORIZONTAL)
    mainSizer.Add(listSizer, 0, wx.EXPAND, 0)
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
      
class PluginSelectionWizard (Hook, Wizard):
  def __init__ (self, *args, **kwargs):
    Wizard.__init__ (self, *args, **kwargs)
    
  def createSubPanels (self):
    self.psc = PluginSelectionControl(self.pool.addWindow ("PluginSelection", PluginSelectionPanel(self)))
    
    
