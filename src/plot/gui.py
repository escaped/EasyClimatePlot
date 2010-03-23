# -*- coding: utf-8 -*-

from mvc.workflow.hook import Hook
from mvc.workflow.viewcontrol import ViewControl
from mvc.workflow.wizard import Wizard


import plot.walterlieth.gui as pwg

import wx

class PlotIntro (ViewControl):
  def createSubPanels (self):
    self.pool.addWindow ("ChooseType", PlotType (self))
    self.pool.addWindow ("WalterLiethWizard", pwg.WalterLiethWizard (self))

class PlotType (Hook, wx.Panel):
  def __init__ (self, *args, **kwargs):
    wx.Panel.__init__ (self, *args, **kwargs)
    self.parent = args[0]
    
    # self.sizer
    self.sizer = wx.BoxSizer (wx.VERTICAL)

    # three buttons (hehe..)
    self.walterlieth = wx.Button (self, -1, label="Walter-Lieth Klimadiagramm")
    self.contour     = wx.Button (self, -1, label="Isoplethendiagramm")
    self.googlemap   = wx.Button (self, -1, label="Stationen auf Karte einzeichnen")

    # TODO disable for now
    self.contour.Disable ()
    self.googlemap.Disable ()

    self.sizer.Add (self.walterlieth)
    self.sizer.Add (self.contour)
    self.sizer.Add (self.googlemap)

    self.SetSizer (self.sizer)

    self.Bind (wx.EVT_BUTTON, self.onWalterLieth, self.walterlieth)

  def onWalterLieth (self, e):
    self.parent.switchSubPanelByName ("WalterLiethWizard")

