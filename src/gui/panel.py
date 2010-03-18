# -*- coding: utf-8 -*-

'''Submodules should use panels to interact with the user.'''

import wx

class Panel1 (wx.Panel):
  def __init__ (self, parent, text):
    wx.Panel.__init__ (self, parent)
    self.lbltext = wx.StaticText(self, label=str (text))

class Workflow (wx.Panel):
  def createSubPanels (self):
    self.subPanelsByName[1] = Panel1 (self, 1)
    self.subPanelsByName[2] = Panel1 (self, 2)
    self.subPanelsByName[3] = Panel1 (self, 3)
    #raise NotImplementedError, "Please implement in deriving classes"

  #########
  # constructor
  #########
  def __init__ (self, parent):
    wx.Panel.__init__ (self, parent)
    self.currentPanel  = None
    self.currentNumber = 0
    # subPanels collection as a simple list
    self.subPanels = []
    # subPanels collection as an assoc. array -
    # this one has to be filled in createSubPanels
    self.subPanelsByName = {}

  def Create (self):
    # sizers
    self.mainSizer = wx.GridBagSizer (hgap = 1, vgap = 2)
    self.buttonSizer = wx.GridBagSizer (hgap = 2, vgap = 1)

    self.mainSizer.Add (self.buttonSizer, pos = (1,0))

    # back and forward buttons
    self.back = wx.Button (self, label = "Zurück")
    self.forward = wx.Button (self, label = "Weiter")

    self.Bind (wx.EVT_BUTTON, self.onBack, self.back)
    self.Bind (wx.EVT_BUTTON, self.onForward, self.forward)

    # add buttons to buttonSizer
    self.buttonSizer.Add (self.back, pos = (0,0))
    self.buttonSizer.Add (self.forward, pos = (0,1))

    # create the subpanels
    self.createSubPanels ()

    # create the list of subpanels
    # TODO make sure, that the order is preserved!
    self.subPanels = [self.subPanelsByName[i] for i in self.subPanelsByName]

    # make sure, that none of the subpanels is shown
    for panel in self.subPanels:
      panel.Show (False)

    # switch to first subpanel
    self.switchSubPanel (self.currentNumber)

    self.SetSizerAndFit (self.mainSizer)

  def switchSubPanel (self, number):
    if number < 0 or number > len (self.subPanels):
      # throw a bad exception
      # TODO hier sollte eine sinnvolle Fehlermeldung erscheinen
      raise IndexError ("Hier sollte eine sinnvolle Fehlermeldung stehen")
    self.currentNumber = number

    if number - 1 < 0:
      self.back.Disable ()
    else:
      self.back.Enable ()

    if number + 2 > len (self.subPanels):
      self.forward.Disable ()
    else:
      self.forward.Enable ()

    if self.currentPanel:
      self.mainSizer.Detach (self.currentPanel)
      self.currentPanel.Show (False)

    self.currentPanel = self.subPanels[number]

    self.mainSizer.Add (self.currentPanel, pos = (0,0))
    self.currentPanel.Show (True)
    self.mainSizer.Layout ()

    self.Layout ()

  def getSubPanelByName (self, name):
    return self.subPanelsByName[name]

  #########
  # event handling
  #########
  def onBack (self, e):
    self.switchSubPanel (self.currentNumber - 1)
  
  def onForward (self, e):
    self.switchSubPanel (self.currentNumber + 1)

