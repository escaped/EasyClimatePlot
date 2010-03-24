import wx

class Notebook (wx.Notebook):
  '''Offers adding of categories and subcategories.'''

  def __init__ (self, *args, **kwargs):
    wx.Notebook.__init__ (self, *args, **kwargs)
    self.categories = {}

  def addItem (self, category, item):
    # item must be of type wx.Panel
    # TODO vielleicht besser plugin?
    if not isinstance (item, wx.Panel):
      raise TypeError, "The given item must be of type wx.Panel"

    try:
      self.categories[category].append (item)
    except KeyError:
      self.categories[category] = []
      self.categories[category].append (item)
      self.AddPage (CategoryPage (self), str (category))


class CategoryPage (wx.Panel):
  def __init__ (self, *args, **kwargs):
    wx.Panel.__init__ (self, *args, **kwargs)



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
