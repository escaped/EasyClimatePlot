'''A simple textctrl, which implements the necessary functions to allow print >>window,
string.'''


import wx

class OutputCtrl (wx.TextCtrl):
  def __init__ (self, *args, **kwargs):
    wx.TextCtrl.__init__ (self, *args, **kwargs)

  def write (self, string):
    '''write (string) appends the given string to the TextCtrl.'''
    self.AppendText (string)
