# -*- coding: utf-8 -*-
'''Submodules should use panels to interact with the user.'''

import wx
from main.workflow.viewcontrol import ViewControl

class Wizard (ViewControl):
  def __init__(self, *args, **kwargs):
    ViewControl.__init__ (self, *args, **kwargs)

    # back and forward buttons
    self.back = wx.Button (self, label = "Zurück")
    self.forward = wx.Button (self, label = "Weiter")

    self.Bind (wx.EVT_BUTTON, self.onBack, self.back)
    self.Bind (wx.EVT_BUTTON, self.onForward, self.forward)

    # additional sizer
    self.buttonSizer = wx.BoxSizer (wx.HORIZONTAL)

    self.mainSizer.Add (self.buttonSizer)

    # add buttons to buttonSizer
    self.buttonSizer.Add (self.back)
    self.buttonSizer.Add (self.forward)

  def switchSubPanelByID (self, number):
    if number < self.pool.lower_bound or number > self.pool.upper_bound:
      # TODO hier sollte eine sinnvolle Fehlermeldung erscheinen
      raise IndexError ("Hier sollte eine sinnvolle Fehlermeldung stehen")   

    if ViewControl.switchSubPanelByID (self, number):
      self.currentNumber = number
      if number - 1 < self.pool.lower_bound:
        self.back.Disable ()
      else:
        self.back.Enable ()

      if number + 2 > self.pool.upper_bound:
        self.forward.Disable ()
      else:
        self.forward.Enable ()
      # TODO Update Layout
  
  def switchSubPanelByName  (self, name):
    self.switchSubPanelByID (self.pool.getWindowIndex (name))

  #########
  # event handling
  #########
  def onBack (self, e):
    self.switchSubPanelByID (self.currentNumber - 1)
  
  def onForward (self, e):
    self.switchSubPanelByID (self.currentNumber + 1)

