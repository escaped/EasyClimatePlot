import wx
from main.workflow.hook import Hook

from eventhandling.eventpool import EventPool

class Panel (Hook, wx.Panel, EventPool):
  '''Panel is a abstract base class which enables subscribing to events.'''
  # TODO dokumentieren!

  def __init__ (self, *args, **kwargs):
    wx.Panel.__init__ (self, *args, **kwargs)
    EventPool.__init__ (self)
