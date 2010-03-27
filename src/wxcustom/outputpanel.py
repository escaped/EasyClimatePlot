'''A panel which makes use of outputctrl.'''

import wx
from panel import Panel
import outputctrl


class OutputPanel (Panel):
  def __init__ (self, *args, **kwargs):
    Panel.__init__ (self, *args, **kwargs)
    self.sizer = wx.BoxSizer () 
    self.textctrl = outputctrl.OutputCtrl(self)
    self.sizer.Add (self.textctrl, -1, wx.EXPAND, 0)
    self.SetSizer (self.sizer)
    self.Layout ()

  def write (self, string):
    self.textctrl.write (string)


# test cases

def test ():
  app = wx.App (False)
  frame = wx.Frame (None)
  op = OutputPanel (frame)
  frame.Show ()

  print >>op, "muahahahaha\n"

  app.MainLoop ()


if __name__ == "__main__":
  test ()

