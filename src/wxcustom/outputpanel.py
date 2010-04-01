'''A panel which makes use of outputctrl.'''

import wx
from panel import Panel
import outputctrl

class OutputPanel (Panel):
  def __init__ (self, *args, **kwargs):
    Panel.__init__ (self, *args, **kwargs)
    self.parent = args[0]

    self.sizer = wx.BoxSizer () 
    self.textctrl = outputctrl.OutputCtrl(self, style=wx.TE_MULTILINE|wx.TE_AUTO_SCROLL)
    self.sizer.Add (self.textctrl, -1, wx.EXPAND, 0)
    self.SetSizer (self.sizer)
    self.Layout ()

  def write (self, string):
    self.textctrl.write (string)
    self.parent.Show (True)


# test cases

def test ():
  app = wx.App (False)
  frame = wx.Frame (None)
  op = OutputPanel (frame)
  frame.Show ()

  print >>op, "muahahahaha"

  app.MainLoop ()


if __name__ == "__main__":
  test ()

