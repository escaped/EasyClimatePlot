'''A frame making use of outputpanel.'''

import wx
import outputpanel

class OutputFrame (wx.Frame):
  def __init__ (self, *args, **kwargs):
    wx.Frame.__init__ (self, *args, **kwargs)

    self.out = outputpanel.OutputPanel (self)

    self.Bind (wx.EVT_CLOSE, self.onClose, self)

  def onClose (self, evt):
    print "ha"
