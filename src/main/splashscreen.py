# -*- coding: utf-8 -*-

import wx
import os

# TODO
# taken from http://wiki.wxpython.org/SplashScreen
class Splashy (wx.SplashScreen):
  def __init__ (self, parent = None):
    aBitmap = wx.Image(name = os.path.join ("img","splash.png")).ConvertToBitmap()
    splashStyle = wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT
    splashDuration = 2000 # milliseconds
    # Call the constructor with the above arguments in exactly the
    # following order.
    wx.SplashScreen.__init__(self, aBitmap, splashStyle,
                             splashDuration, parent)
    self.Bind(wx.EVT_CLOSE, self.OnExit)

    wx.Yield()

  def OnExit(self, evt):
    self.Hide()
    # MyFrame is the main frame.
    evt.Skip()  # Make sure the default handler runs too...
    self.Destroy ()
