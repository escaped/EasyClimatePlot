# -*- coding: utf-8 -*-
'''
Created on Mar 23, 2010

@author: alex
'''
from mvc.control import Control
from mvc.workflow.viewcontrol import ViewControl

import wx
from wxcustom.panel import Panel
from wxcustom.error import ErrorMessage

from pluginmanager import PluginManager, WizardPlugin

class NotEmptyListBoxValidator (wx.PyValidator):
  def __init__(self, msg = "Field cannot be empty."):
    wx.PyValidator.__init__(self)    
    self.errorMsg = msg
  
  def TransferToWindow(self):
    return True # Prevent wxDialog from complaining.

  def TransferFromWindow(self):
    return True # Prevent wxDialog from complaining.
    
  def Clone(self):
    return NotEmptyListBoxValidator(self.errorMsg)
  
  def Validate(self, win):
    item = self.GetWindow()
    value = item.GetStringSelection()
    
    if len(value) == 0:
      ErrorMessage (self.errorMsg)
      item.SetFocus()
      return False
    
    return True

class PluginSelectionControl (Control):
  def __init__ (self, view, viewcontrol, type):
    Control.__init__ (self, view)
    self.vc = viewcontrol    
    self.pm = PluginManager.getInstance()
    
    if type in [WizardPlugin.T_INPUT, WizardPlugin.T_OUTPUT]:
      self.type =  type  # TODO Parameter
    else:
      raise Exception("Invalid PluginType")
    
    
  def onActivate(self):
    if self.type == WizardPlugin.T_OUTPUT:
      print "setting out"
      self.view.setPlugins(self.pm.getOutputPlugins().keys())
    else:
      print "setting in"
      self.view.setPlugins(self.pm.getInputPlugins().keys())
      
    return True
    
  def onDeactivate(self):
    ''' Check Input '''
    # nothing todo cause of onContinue
    return True
  
  def onContinue(self, *args, **kwargs):
    if self.view.Validate():
      # add view to ViewControl
      pluginName = self.view.list.GetStringSelection()
      if pluginName != None:
        try: 
          # TODO ist unabhŠngig vom Typ
          if self.type == WizardPlugin.T_OUTPUT:
            plugin = self.pm.getOutputPlugins()[pluginName]
          else:
            plugin = self.pm.getInputPlugins()[pluginName]
            
          self.vc.pool.addWindow (plugin.getName(), plugin.getWizard(self.vc))
          self.vc.switchSubPanelByName(plugin.getName())
          selv.vc.pool[plugin.getName ()].initSubPanel ()
        except KeyError:
          print "unexpected error: no valid plugin selected"
      
       
  def onListSelection(self, *args, **kwargs):
    pluginName = self.view.list.GetStringSelection()
    print "Selected: %s" %(pluginName)
    if pluginName != None:
      try: 
        # TODO ist unabhängig vom Typ
        if self.type == WizardPlugin.T_OUTPUT:
          plugin = self.pm.getOutputPlugins()[pluginName]
        else:
          plugin = self.pm.getInputPlugins()[pluginName]
      except KeyError:
        # TODO hier wäre eine Warnung auch angebracht
        self.clearInfo()
        return
      
      self.view.lblName.SetLabel(plugin.getName())
      self.view.lblVersion.SetLabel(plugin.getVersion())
      self.view.lblAuthor.SetLabel(plugin.getAuthor())
      self.view.lblDescription.SetLabel(plugin.getDescription())   
    else:
      self.clearInfo()
  
  def clearInfo(self):
      self.view.lblName.SetLabel("")
      self.view.lblVersion.SetLabel("")
      self.view.lblDescription.SetLabel("")   
      self.view.lblAuthor.SetLabel("")
      
  def setPluginType(self, type):
    self.type = type
    self.onActivate()
  
# TODO beim rücksprung sollte man auch ein anderes plugin wählen können.  
class PluginSelectionPanel(Panel):
  def __init__(self, *args, **kwargs):
    Panel.__init__ (self, *args, **kwargs)   
    
    # List
    listSizer = wx.BoxSizer(wx.VERTICAL)
    self.list = wx.ListBox(choices=[], parent=self, size=wx.Size(150, 200), validator=NotEmptyListBoxValidator("Please select a plugin."))
    self.list.Bind(wx.EVT_LISTBOX, self["ListSelection"])
    
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
    
    # VerticalSize for btn
    btnSelect = wx.Button (self, -1, "use Plugin")
    btnSelect.Bind(wx.EVT_BUTTON, self["Continue"])
    
    btnSizer = wx.BoxSizer(wx.VERTICAL)
    btnSizer.Add(mainSizer, 0, wx.EXPAND, 0)
    btnSizer.Add(btnSelect, 0, wx.EXPAND, 0)
    
    self.SetSizerAndFit(btnSizer)
  
  def setPlugins(self, plugins=[]):
    self.list.AppendItems(plugins)
      
class PluginSelection(ViewControl):
  def __init__(self, *args, **kwargs):
    self.type = args[1]
    ViewControl.__init__(self, *args, **kwargs)
      
  def createSubPanels (self):
    self.psc = PluginSelectionControl(self.pool.addWindow ("PluginSelection", PluginSelectionPanel(self)), self, self.type)
    
    
