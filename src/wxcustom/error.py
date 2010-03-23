'''Provides error message dialogs.'''
import wx

ERROR_TITLE = "Fehler"

class ErrorMessage (wx.MessageDialog):
  def __init__ (self, errormsg):
    wx.MessageDialog.__init__ (self, None, str(errormsg), ERROR_TITLE, wx.OK)
    self.ShowModal ()
    self.Destroy ()

