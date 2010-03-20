# -*- coding: utf-8 -*-

# TODO better comment
# custom implementation of http://www.daniweb.com/forums/post650657.html#post650657

import wx

# TODO ist das nötig?
MAX_ROWS = 1000

class DataListBox (wx.ListCtrl):
  '''Inherits from DataListBox. This class should work similar to a .Net
  DataGridView.'''

  def __init__ (self, parent, columns = None):
    '''Parameter: columns = list of column names (strings)'''
    # TODO style anpassen
    # TODO size ist kacke. geht das nicht anders?
    wx.ListCtrl.__init__ (self, parent, style =
        wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_HRULES, size = (400, 100))

    # create columns
    self.columns = columns
    self.__createcolumns__ (columns)

    self.data = []

  def __createcolumns__ (self, columns):
    for id, column in zip (xrange (0, len (columns)), columns):
      self.InsertColumn (id, column)

  def AddData (self, dataDict, keys):
    '''Wraps AddManyData (dataDictList)'''
    self.AddManyData ([dataDict])

  # keys: the list of needed keys in the _right_ order
  def AddManyData (self, dataDictList, keys):
    self.data.extend (dataDictList)
    # set max_rows, change if need be
    for id, item in zip (xrange (0, len (dataDictList)), dataDictList):
      index = self.InsertStringItem(MAX_ROWS, "empty")
      i = 0
      for key in keys:
        self.SetStringItem (index, i, str(item[key]))
        i += 1
      # needed by GetItemData()
      self.SetItemData(index, id)

  def getSelected (self):
    selected = []
    i = self.GetFirstSelected ()
    while i != -1:
      selected.append (i)
      i = self.GetNextItem (i,
             wx.LIST_NEXT_ALL,
             wx.LIST_STATE_SELECTED)
    return [self.data[i] for i in selected]

  def clear (self):
    pass

# usage test

if __name__ == "__main__":
  app = wx.App (False)
  frame = wx.Frame (None, size= (-1,300))
  dcl = DataListBox (frame, ["name", "age", "weight"])

  data = [
      {"name" : 'Heidi Kalumpa'    , "age" : '36', "weight" : '127'},
      {"name" : 'Frank Maruco'     , "age" : '27', "weight" : '234'},
      {"name" : 'Larry Pestraus'   , "age" : '19', "weight" : '315'},
      {"name" : 'Serge Romanowski' , "age" : '59', "weight" : '147'},
      {"name" : 'Carolus Arm'      , "age" : '94', "weight" : '102'},
      {"name" : 'Michel Sargnagel' , "age" : '21', "weight" : '175'}
  ]
  # add data
  dcl.AddManyData (data, ["age", "name", "weight"])

  # event
  # if one is selected, print all selected
  def f (event):
    print dcl.getSelected ()
  dcl.Bind (wx.EVT_LIST_ITEM_SELECTED, lambda x: f(x))

  frame.Show ()
  app.MainLoop ()
