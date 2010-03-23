'''Provides error message dialogs.'''
import wx.lib.dialogs

ERROR_TITLE = "Fehler"

def ErrorMessage (errormsg):
  '''Just a proxy for wx.lib.dialogs.alertDialog'''
  wx.lib.dialogs.alertDialog (None, errormsg, ERROR_TITLE)

