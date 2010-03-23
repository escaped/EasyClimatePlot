# -*- coding: utf-8 -*-

from control import PlotTypeControl

from mvc.workflow.hook import Hook
from mvc.workflow.viewcontrol import ViewControl
from mvc.workflow.wizard import Wizard

from wxcustom.panel import Panel


import plot.walterlieth.gui as pwg

import wx

class PlotIntro (ViewControl):
  def createSubPanels (self):
    ptview = PlotType (self)

    self.pool.addWindow ("ChooseType", ptview)
    choose_control = PlotTypeControl (ptview)

    self.pool.addWindow ("WalterLiethWizard", pwg.WalterLiethWizard (self))

class PlotType (Panel):
  def __init__ (self, *args, **kwargs):
    Panel.__init__ (self, *args, **kwargs)
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

    # bind events
    self.Bind (wx.EVT_BUTTON, self["WalterLieth"], self.walterlieth)


