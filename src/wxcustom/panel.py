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
    self["Activate"]
    self["Deactivate"]

  def activate (self):
    '''Every deriving class should call this function to fire the right event!'''
    return self["Activate"].fire ()

  def deactivate (self):
    '''Every deriving class should call this function to fire the right event!'''
    return self["Deactivate"].fire ()
    

