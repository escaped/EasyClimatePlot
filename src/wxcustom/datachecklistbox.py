# -*- coding: utf-8 -*-
import wx

# TODO column names

class DataCheckListbox (wx.CheckListBox):
  '''Inherits from DataCheckListbox. This class should work similar to a .Net
  DataGridView.'''

  def __init__ (self, *args, **kwargs):
    # TODO proper comment
    wx.CheckListBox.__init__ (self, *args, **kwargs)
    self.parent = args[0]
    self.data = []
    self.selected = []

    # bind to event
    self.Bind (wx.EVT_CHECKLISTBOX, self.onCheck, self)
    self.Layout ()

  def onCheck (self, e):
    # NOTE: e.GetInt returns the actual index of the selected item,
    # not like lctChooseStation.GetSelections () ...
    if self.IsChecked (e.GetInt ()):
      self.selected.append (self.data[e.GetInt ()])
    else:
      del self.selected[self.data.index (self.selected[e.GetInt ()])]

  def AddData (self, dataDict, columnList):
    '''dataDict: Dictionary containing the data.
    columnList: List of keys'''
    self.data.append (dataDict)
    self.AppendAndEnsureVisible ('\t'.join([dataDict [key] for key in columnList]))

    self.Layout ()

  def AddManyData (self, dataDictList, columnList):
    '''Does the same as AddData, but for a list of dicts.'''
    for item in dataDictList:
      self.AddData (item, columnList)

  def getSelected (self):
    return self.selected

  def clear (self):
    # TODO die alte suche muss richtig gelöscht werden! inklusive der markierungen!
    self.data = []
    self.selected = []
    self.Layout ()
