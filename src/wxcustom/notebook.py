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
      self.AddPage (self.categoryPages[category], str (category))

      self.categories[category].append (item)
      self.categoryPages[category].listctrl.InsertStringItem (str(item))

class CategoryPage (wx.Panel):
  def __init__ (self, *args, **kwargs):
    wx.Panel.__init__ (self, *args, **kwargs)
    self.listctrl = wx.ListCtrl (self)

# usage test


if __name__ == "__main__":

  class TestPanel (wx.Panel):
    def __init__ (self, parent):
      wx.Panel.__init__ (self, parent)
      self.txt = wx.TextCtrl(self, -1, "hallo")
  
  app   = wx.App (False)
  frame = wx.Frame (None)
  nb    = Notebook (frame)

  testpanel = TestPanel (nb)

  nb.addItem ("hallo", testpanel)

  frame.Show ()
  app.MainLoop ()
