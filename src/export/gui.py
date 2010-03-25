# -*- coding: utf-8 -*-

from mvc.workflow.hook import Hook
from mvc.workflow.viewcontrol import ViewControl
from mvc.workflow.wizard import Wizard


import export.noaa.batchgeocode as enb

import wx

class ExportIntro (ViewControl):
  def createSubPanels (self):
    self.pool.addWindow ("ChooseType", PlotType (self))
    # TODO
    #self.pool.addWindow ("NOAA_Wizard", enb.NOAA (self))

# TODO WEnn das implementiert wird, sollte das mit ins NOAA Plugin dir udn entsprechendes Plugin in der __init__.py definiert werden!!!
class PlotType (Hook, wx.Panel):
  def __init__ (self, *args, **kwargs):
    wx.Panel.__init__ (self, *args, **kwargs)
    self.parent = args[0]
    
    # self.sizer
    self.sizer = wx.BoxSizer (wx.VERTICAL)

    # three buttons (hehe..)
    self.noaa  = wx.Button (self, -1, label="NOAA Stationsdaten")

    self.sizer.Add (self.noaa)

    self.SetSizer (self.sizer)
    #self.Bind (wx.EVT_BUTTON, self.onWalterLieth, self.walterlieth)

