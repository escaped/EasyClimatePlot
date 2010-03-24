import wx

class Notebook (wx.Notebook):
  '''Offers adding of categories and subcategories.'''

  def __init__ (self, *args, **kwargs):
    wx.Notebook.__init__ (self, *args, **kwargs)
    # TODO nur ein dict dafr
    self.categories = {}
    self.categoryPages = {}

  def addItem (self, category, item):
    # item must be of type wx.Panel
    # TODO vielleicht besser plugin?
    if not isinstance (item, wx.Panel):
      raise TypeError, "The given item must be of type wx.Panel"

    # "add" each item to a list..
    try:
      self.categories[category].append (item)
      self.categoryPages[category].listctrl.Append (str(item))
    except KeyError:
      self.categories[category] = []
      self.categoryPages[category] = CategoryPage (self)
      self.AddPage (self.categoryPages[category], str (category), wx.EXPAND)

      self.categories[category].append (item)
      self.categoryPages[category].insertString (str(item))


class CategoryPage (wx.Panel):
  def __init__ (self, *args, **kwargs):
    wx.Panel.__init__ (self, *args, **kwargs)
    self.sizer = wx.BoxSizer ()
    self.listctrl = wx.ListCtrl (self)
    # TODO diese sizer sind eine komische sache..
    # mit dem unteren aufruf wird das zumindest vertikal expandiert
    self.sizer.Add (self.listctrl, -1, wx.EXPAND,0)

    self.SetSizerAndFit (self.sizer)
    self.SetAutoLayout (True)

  def insertString(self, string):
    self.listctrl.InsertStringItem (wx.ID_NEW, string)

# usage test


if __name__ == "__main__":

  class TestPanel (wx.Panel):
    def __init__ (self, parent):
      wx.Panel.__init__ (self, parent)
      self.txt = wx.TextCtrl(self, -1, "hallo", style=wx.EXPAND)
  
  app   = wx.App (False)
  frame = wx.Frame (None)
  nb    = Notebook (frame)

  testpanel = TestPanel (nb)
  nb.addItem ("hallo", testpanel)


  frame.Show ()
  app.MainLoop ()
