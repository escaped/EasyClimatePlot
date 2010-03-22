import wx
from main.workflow.hook import Hook

from eventhandling.eventpool import EventPool
from eventhandling.event import Event

class Panel (Hook, wx.Panel, EventPool):
  '''Panel is a abstract base class which enables subscribing to events.'''
  def __init__ (self, *args, **kwargs):
    wx.Panel.__init__ (self, *args, **kwargs)
    EventPool.__init__ (self)

    # some basic events needed by every panel
    self["activate"]
    self["deactivate"]

  def activate (self):
    '''Every deriving class should call this function to fire the right event!'''
    self["activate"].fire ()
    return True

  def deactivate (self):
    '''Every deriving class should call this function to fire the right event!'''
    self["deactivate"].fire ()
    return True

